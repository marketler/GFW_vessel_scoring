"""
Vessel statistics
"""

import sys
import datetime
import itertools
import numpy
import rolling_measures


def hours_per_day(latitude, day_of_year):
    # From https://www.quora.com/How-can-you-calculate-the-length-of-the-day-on-Earth-at-a-given-latitude-on-a-given-date-of-the-year
    latitude = numpy.radians(latitude)
    # compute declination using approx from
    # https://en.wikipedia.org/wiki/Position_of_the_Sun
    # XXX check that day_of_year is correcly 0 or 1 referenced
    delta = numpy.radians(-23.44 * numpy.cos(numpy.radians((360.0 / 365.0) * (day_of_year + 10.0))))
    cosh = -numpy.tan(latitude) * numpy.tan(delta)
    fill = (1.0 + numpy.sign(cosh)) * 90.0 # 0 or 180 depending on sign of cosh
    h = numpy.where(abs(cosh) > 1, fill, numpy.arccos(cosh))
    return 2.0 * numpy.degrees(h) / 15.0

def daylight(longitude, latitude, timestamp):
    day_of_year = timestamp.timetuple().tm_yday - 1
    daylight = hours_per_day(latitude, day_of_year)

    local_time = timestamp + datetime.timedelta(longitude / 360.0)
    noon = datetime.datetime.combine(local_time.date(), datetime.time(12, 0, 0))

    hours_from_noon = abs((local_time - noon).total_seconds() / 60.0 / 60.0)

    return daylight / 2.0 > hours_from_noon

def localtime(longitude, timestamp):
    local_timestamp = timestamp + datetime.timedelta(longitude / 360.0)
    return (local_timestamp - datetime.datetime.combine(local_timestamp.date(), datetime.time(0, 0, 0))).total_seconds() / 60. / 60.

def AddPointMeasures(messages):
    for msg in messages:
        if msg.get('lat', None) is not None and msg.get('lon', None) is not None and msg.get('timestamp', None) is not None:
            # msg['measure_localtime'] = localtime(msg['lon'], msg['timestamp'])
            msg['measure_daylight'] = [0, 1][daylight(msg['lon'], msg['lat'], msg['timestamp'])]
        yield msg

def AddNormalizedMeasures(messages):
    for row in messages:
        heading = row.get('heading')
        if heading is not None:
            row['measure_heading'] = heading / 360.0

        course = row.get('course')
        if course is not None:
            row['measure_course'] = course / 360.0
            row['measure_cos_course'] = numpy.cos(numpy.radians(course)) / numpy.sqrt(2)
            row['measure_sin_course'] = numpy.sin(numpy.radians(course)) / numpy.sqrt(2)

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
                row['measure_distance_from_port'] = min(1.0, distance_from_port / 30.0) # XXX check units of distance from port (might be meters!)
        yield row


class AddWindowMeasures(object):

    """
    Adds window based measures to track points.  Input is sorted by mmsi,track,timestamp.
    Requires two handles to the _same_ stream of messages for the two ends of the window.
    """

    def __init__(self, messages, window_size=datetime.timedelta(seconds=60 * 60), offset=datetime.timedelta(0.0)):
        """
        Iterate to get messages with additional measures.

        Parameters
        ----------
        stream: iter
            GPSd messages.
        window_size : datetime.timedelta, optional
            Size of window in seconds.
        offset: float ]0, 1[
            Offset from the end of the window.
        """
        stream1, stream2, stream3 = itertools.tee(messages, 3)
        self.startIn = self.load_lines(stream1)
        self.middleIn = self.load_lines(stream2)
        self.endIn = self.load_lines(stream3)
        self.current_track = None
        self.window_size = window_size
        self.offset = offset
        self.startidx = -1
        self.endidx = -1
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

    def get_measures(self):
        s = self.stats.get()
        # # Knots...
        # s['measure_pos'] = (s['measure_pos'] * 60) / (self.window_size.total_seconds() / 60 / 60)
        # # Normalize to "normal" vessel speed
        # s['measure_pos'] /= 17.0
        # s['measure_pos'] = min(1.0, s['measure_pos'])

        s = {"%s_%s" % (key, int(self.window_size.total_seconds())): value
             for key, value in s.iteritems()}

        EPSILON = 1e-3
        for key, value in s.items():
            if 'stddev' in key:
                s[key + "_log"] = float(numpy.log10(value + EPSILON))

        return s

    def start_track(self):
        self.current_track = self.middle
        self.stats = rolling_measures.Stats({
            # 'speed_avg' : rolling_measures.Stat("speed", rolling_measures.Avg),
            'measure_count' :  rolling_measures.Stat('measure_speed', rolling_measures.Count),
            "measure_daylightavg": rolling_measures.Stat("measure_daylight", rolling_measures.Avg),
            "measure_coursestddev": rolling_measures.StatSum(
                rolling_measures.Stat("measure_cos_course", rolling_measures.StdDev),
                rolling_measures.Stat("measure_sin_course", rolling_measures.StdDev)),
            "measure_speedstddev": rolling_measures.Stat("measure_speed", rolling_measures.StdDev),
            "measure_courseavg": rolling_measures.Stat("measure_course", rolling_measures.Avg),
            "measure_speedavg": rolling_measures.Stat("measure_speed", rolling_measures.Avg),
            "measure_latavg": rolling_measures.Stat("lat", rolling_measures.Avg),
            "measure_lonavg": rolling_measures.Stat("lon", rolling_measures.Avg),
            "measure_pos": rolling_measures.StatSum(
                rolling_measures.Stat("lat", rolling_measures.StdDev),
                rolling_measures.Stat("lon", rolling_measures.StdDev))
        })

    def row_in_current_track(self, row):
        return (self.current_track and
                row.get('mmsi', None) == self.current_track.get('mmsi', None) and
                row.get('seg_id', None) == self.current_track.get('seg_id', None))

    def process(self):

        def valid(x):
            return (x and
                    x.get('timestamp') is not None and
                    x.get('course') is not None and                    
                    x.get('speed') is not None 
                    )

        for self.middleidx, self.middle in self.middleIn:
            if valid(self.middle):

                if not self.row_in_current_track(self.middle):
                    while self.startidx < self.middleidx:
                        self.startidx, self.start = self.startIn.next()
                    while self.endidx < self.middleidx:
                        self.endidx, self.end = self.endIn.next()
                    self.start_track()

                while self.row_in_current_track(self.end):
                    if valid(self.end):
                        if self.end['timestamp'] - self.middle['timestamp'] > self.offset:
                            break
                        self.stats.add(self.end)
                    try:
                        self.endidx, self.end = self.endIn.next()
                    except StopIteration:
                        break


                while self.row_in_current_track(self.start):
                    if valid(self.start):
                        if self.middle['timestamp'] - self.start['timestamp']  <= (self.window_size - self.offset):
                            break
                        self.stats.remove(self.start)
                    try:
                        self.startidx, self.start = self.startIn.next()
                    except StopIteration:
                        break


                self.middle.update(self.get_measures())

            yield self.middle


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
            if not self.current_track or msg.get('mmsi', None) != self.current_track.get('mmsi', None) or msg.get('seg_id', None) != self.current_track.get('seg_id', None):
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



def AddMeasures(messages, windows = [900, 1800, 3600, 10800, 21600, 43200, 86400],
        offsets = [0, 0, 0, 0, 0, 0, 0]):
    messages = AddPointMeasures(messages)

    messages = AddNormalizedMeasures(messages)

    for window_size, delta in zip(windows, offsets):
        messages = AddWindowMeasures(messages, datetime.timedelta(seconds=window_size), 
                datetime.timedelta(seconds=delta))

    return messages
