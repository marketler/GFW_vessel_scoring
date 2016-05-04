# Find the root directory of vessel-scoring, if running directly from git
import sys, os.path; sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import vessel_scoring.add_measures
import vessel_scoring.utils
import numpy
import itertools
import datetime

orig = numpy.load(sys.argv[1])['x']

messages = vessel_scoring.utils.numpy_to_messages(orig)
messages = vessel_scoring.add_measures.AddMeasures(messages)
res = vessel_scoring.utils.messages_to_numpy(messages, len(orig))

numpy.savez_compressed(sys.argv[2], x=res)
