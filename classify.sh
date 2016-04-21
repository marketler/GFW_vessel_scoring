#! /bin/bash

rm classified.msg classified.json schema.json classified-filtered.msg classified-filtered.csv classified-filtered.npz

python process.py
benthos etl filtersplit -f "row.get('classification', None) is not None" classified.msg classified-filtered.msg
python tonumpy.py classified-filtered.msg classified-filtered.npz
