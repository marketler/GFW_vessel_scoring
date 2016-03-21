#! /usr/bin/env python

import numpy
import gpsdio
import datetime

cols = ["latitude", "longitude", "classification","distance_to_port","distance_to_shore","measure_course_diff","measure_courseavg_10800","measure_courseavg_1800","measure_courseavg_21600","measure_courseavg_3600","measure_courseavg_43200","measure_courseavg_86400","measure_coursestddev_10800","measure_coursestddev_1800","measure_coursestddev_21600","measure_coursestddev_3600","measure_coursestddev_43200","measure_coursestddev_86400","measure_distance_to_port","measure_heading_diff","measure_new_score_10800","measure_new_score_1800","measure_new_score_21600","measure_new_score_3600","measure_new_score_43200","measure_new_score_86400","measure_pos_10800","measure_pos_1800","measure_pos_21600","measure_pos_3600","measure_pos_43200","measure_pos_86400","measure_speed","measure_speed_diff","measure_speedavg_10800","measure_speedavg_1800","measure_speedavg_21600","measure_speedavg_3600","measure_speedavg_43200","measure_speedavg_86400","measure_speedstddev_10800","measure_speedstddev_1800","measure_speedstddev_21600","measure_speedstddev_3600","measure_speedstddev_43200","measure_speedstddev_86400","speed","heading","course","measure_course","timestamp","timestamp_diff","mmsi"]

length = 0

with gpsdio.open("classified-filtered.msg") as f:
     for row in f:
          length += 1

x = numpy.zeros(length, dtype=[(name, "f8") for name in cols])

with gpsdio.open("classified-filtered.msg") as f:
     for rownum, row in enumerate(f):
          for col in cols:
               val = row.get(col, numpy.Infinity)
               if isinstance(val, datetime.datetime):
                    val = float(val.strftime("%s"))
               x[col][rownum] = val

numpy.savez_compressed(
    "classified-filtered.npz",
    x=x)
