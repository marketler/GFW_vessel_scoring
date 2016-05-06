# Find the root directory of vessel-scoring, if running directly from git
import sys, os.path; sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import vessel_scoring.add_measures
import vessel_scoring.utils
import numpy
import itertools
import datetime
import numpy as np

orig = numpy.load(sys.argv[1])['x']

if len(sys.argv) == 4:
    default = int(sys.argv[3])
    print "Replacing Infs and NaNs with", default
    is_missing = np.isnan(orig['classification']) | np.isinf(orig['classification'])
    orig['classification'][is_missing] = default

# Sort by mmsi, then by timestamp
orig = orig[np.lexsort((orig['timestamp'], orig['mmsi']))]
messages = vessel_scoring.utils.numpy_to_messages(orig)
messages = vessel_scoring.add_measures.AddMeasures(messages, windows=[43200])
res = vessel_scoring.utils.messages_to_numpy(messages, len(orig))

numpy.savez_compressed(sys.argv[2], x=res)
