#! /bin/bash

rm classified.msg classified.json schema.json
python process.py
benthos etl filtersplit -f "row.get('classification', None) is not None" classified.msg classified-filtered.msg
benthos etl tocsv -c measure_new_score,classification,classification_longliner,classification_purse_seine,speed,measure_coursestddev,measure_speedstddev,measure_speedavg,distance_to_shore classified-filtered.msg classified-filtered.csv

#benthos etl tobigquery -c \
#  mmsi,lon,lat,timestamp,sigma,measure_new_score,classification,classification_longliner,classification_purse_seine,heading,turn,course,speed,series,seriesgroup,gridcode,interval,type,next_gridcode,extra \
#  classified.msg classified.json schema.json

#sutil -m cp  classified.json gs://world-fishing-827/scratch/egil/classified-tracks.json
