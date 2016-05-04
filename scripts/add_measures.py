# Find the root directory of vessel-scoring, if running directly from git
import sys, os.path; sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import vessel_scoring.add_measures
import numpy
import itertools
import datetime

orig = numpy.load(sys.argv[1])['x']

def convert_row(row):
    res = {name:row[name] for name in row.dtype.names}
    res['timestamp'] = datetime.datetime.fromtimestamp(res['timestamp'])
    return res

messages = (convert_row(row) for row in orig)
messages = vessel_scoring.add_measures.AddMeasures(messages)

peek, messages = itertools.tee(messages, 2)
columns = peek.next().keys()
res = numpy.zeros(len(orig), dtype = [(name, 'f8') for name in columns])
for message in messages:
    for column in columns:
        val = message.get(column, None)
        if isinstance(val, datetime.datetime):
            val = float(val.strftime("%s"))
        elif isinstance(val, datetime.timedelta):
            val = val.total_seconds()
        res[column] = val

numpy.savez_compressed(sys.argv[2], x=res)
