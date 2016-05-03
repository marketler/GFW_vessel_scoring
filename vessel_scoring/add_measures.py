"""
Vessel statistics
"""

import gpsdio
import sys
import datetime
import numpy
from numpy import *
from numpy.lib.recfunctions import *
import datetime
import itertools
import numpy
import rolling_measures


def append_field_if_new(x, name):
    if name in x.dtype.names:
        return x
    return append_fields(x, name, [], dtypes='<f8', fill_value=0.0).filled()

def add_measures(x, windowSizes = [1800, 3600, 10800, 21600, 43200, 86400], verbose=True, err=sys.stderr):
    x = x[x['course'] != Inf]
    x = x[x['speed'] != Inf]

    # Sort by mmsi, then by timestamp
    x = x[lexsort((x['timestamp'], x['mmsi']))]

    x = append_field_if_new(x, 'measure_speed')
    x = append_field_if_new(x, 'measure_course')

    # Normalize speed and heading
    speed = x['speed'] / 17.0
    x['measure_speed'] = 1 - where(speed > 1.0, 1.0, speed)
    x['measure_course'] = x['course'] / 360.0

    windowSizes = [1800, 3600, 10800, 21600, 43200, 86400]
    for windowSize in windowSizes:
        x = append_field_if_new(x, 'measure_speedstddev_%s' % windowSize)
        x = append_field_if_new(x, 'measure_speedavg_%s' % windowSize)
        x = append_field_if_new(x, 'measure_coursestddev_%s' % windowSize)
        x = append_field_if_new(x, 'measure_new_score_%s' % windowSize)

        # Calculate rolling stddev/avg of course and speed
        start_idx = 0
        for end_idx in xrange(0, x.shape[0]):
            if verbose and end_idx % 1000 == 0:
                err.write("addmeasures: %s\n" % (end_idx,))
                err.flush()

            while (x['mmsi'][start_idx] != x['mmsi'][end_idx]
                   or x['timestamp'][start_idx] < x['timestamp'][end_idx] - windowSize):
                start_idx += 1
            assert start_idx <= end_idx
            window = x[start_idx:end_idx + 1]   
            x['measure_speedstddev_%s' % windowSize][end_idx] = window['measure_speed'].std()
            x['measure_speedavg_%s' % windowSize][end_idx] = numpy.average(window['measure_speed'])
            x['measure_coursestddev_%s' % windowSize][end_idx] = window['measure_course'].std()

            if isnan(x['measure_coursestddev_%s' % windowSize][end_idx]):
                print "XXXXXX", start_idx, end_idx + 1

    return x


# Streaming API

def AddNormalizedMeasures(messages):
    for row in messages:
        heading = row.get('heading')
        if heading is not None:
            row['measure_heading'] = heading / 360.0

        course = row.get('course')
        if course is not None:
            row['measure_course'] = course / 360.0

        speed = row.get('speed')
        if speed is not None:
            row['measure_speed'] = 1.0 - min(1.0, speed / 17.0)

        turn = row.get('turn')
        if turn is not None:
            try:
                row['measure_turn'] = min(1.0, abs(turn) / 126.0)
            except Exception:
                assert False, "{} {}".format(turn, type(turn))

        # Since `dict.get()` defaults to `None`, `tools.AbsentKey` makes sure we don't
        # add a `distance_from_port = 1` to messages that don't have a value, which
        # are mainly non-posits.

        if 'distance_from_port' in row:
            distance_from_port = row['distance_from_port']
            if distance_from_port is None:
                row['measure_distance_from_port'] = 1.0
            else:
                row['measure_distance_from_port'] = min(1.0, distance_from_port / 30.0)
        yield row


class AddWindowMeasures(object):

    """
    Adds window based measures to track points.  Input is sorted by mmsi,track,timestamp.
    Requires two handles to the _same_ stream of messages for the two ends of the window.
    """

    diffkeys = [
        'lon', 'lat', 'timestamp', 'measure_heading', 'measure_turn',
        'measure_course', 'measure_speed']

    def __init__(self, messages, window_size=datetime.timedelta(seconds=60 * 60)):

        """
        Iterate to get messages with additional measures.

        Parameters
        ----------
        stream: iter
            GPSd messages.
        window_size : datetime.timedelta, optional
            Size of window in seconds.
        """

        stream1, stream2 = itertools.tee(messages, 2)
        self.startIn = self.load_lines(stream1)
        self.endIn = self.load_lines(stream2)
        self.current_track = None
        self.window_size = window_size
        self.startidx = -1
        self._iterator = None

    def __iter__(self):
        if not self._iterator:
            self._iterator = self.process()
        return self._iterator

    def __next__(self):
        return next(self._iterator)

    next = __next__

    def load_lines(self, in_file):
        for idx, line in enumerate(in_file):
            yield idx, line

    def add_measures_to_row(self):
        s = self.stats.get()
        # Knots...
        s['measure_pos'] = (s['measure_pos'] * 60) / (self.window_size.total_seconds() / 60 / 60)
        # Normalize to "normal" vessel speed
        s['measure_pos'] /= 17.0
        s['measure_pos'] = min(1.0, s['measure_pos'])

        s = {"%s_%s" % (key, int(self.window_size.total_seconds())): value
             for key, value in s.iteritems()}

        for key, value in s.items():
            if 'stddev' in key:
                if value == 0.0:
                    s[key + "_log"] = float(numpy.finfo(numpy.dtype("f4")).min)
                else:
                    s[key + "_log"] = float(numpy.log10(value))

        self.end.update(s)

    def start_track(self):
        self.current_track = self.end
        self.prev = None
        self.stats = rolling_measures.Stats({
            "measure_coursestddev": rolling_measures.Stat("measure_course", rolling_measures.StdDev),
            "measure_speedstddev": rolling_measures.Stat("measure_speed", rolling_measures.StdDev),
            "measure_courseavg": rolling_measures.Stat("measure_course", rolling_measures.Avg),
            "measure_speedavg": rolling_measures.Stat("measure_speed", rolling_measures.Avg),
            "measure_latavg": rolling_measures.Stat("lat", rolling_measures.Avg),
            "measure_lonavg": rolling_measures.Stat("lon", rolling_measures.Avg),
            "measure_pos": rolling_measures.StatSum(
                rolling_measures.Stat("lat", rolling_measures.StdDev),
                rolling_measures.Stat("lon", rolling_measures.StdDev))
        })

    def process(self):
        for self.endidx, self.end in self.endIn:

            if not self.current_track or self.end['mmsi'] != self.current_track['mmsi'] or self.end['seg_id'] != self.current_track['seg_id']:
                while self.startidx < self.endidx:
                    self.startidx, self.start = self.startIn.next()
                self.start_track()

            self.stats.add(self.end)

            if 'timestamp' in self.end:
                while (   not self.start
                       or 'timestamp' not in self.start
                       or self.end['timestamp'] - self.start['timestamp'] > self.window_size):
                    if self.start:
                        self.stats.remove(self.start)
                    self.startidx, self.start = self.startIn.next()

            self.add_measures_to_row()

            out = self.end.copy()

            yield out


class AddPairMeasures(object):

    """
    Adds pair based measures to track points.  Input is sorted by mmsi,track,timestamp.
    """

    diffkeys = [
        'lon', 'lat', 'timestamp', 'measure_heading', 'measure_turn',
        'measure_course', 'measure_speed']

    def __init__(self, messages, window_size=datetime.timedelta(seconds=60 * 60)):

        self.messages = messages
        self.current_track = None
        self._iterator = None
        self.prev = None

    def __iter__(self):
        if not self._iterator:
            self._iterator = self.process()
        return self._iterator

    def __next__(self):
        return next(self._iterator)

    next = __next__

    def process(self):
        for msg in self.messages:
            if not self.current_track or msg['mmsi'] != self.current_track['mmsi'] or msg['seg_id'] != self.current_track['seg_id']:
                self.prev = None
                self.current_track = msg

            if self.prev is None:
                self.prev = msg
            msg.update({key + "_diff": abs(msg[key] - self.prev[key])
                             for key in self.diffkeys
                             if key in msg and key in self.prev})
            self.prev = msg

            timestamp_diff = msg.get('timestamp_diff')
            if timestamp_diff is not None:
                msg['timestamp_diff'] = timestamp_diff.total_seconds()

            yield msg

