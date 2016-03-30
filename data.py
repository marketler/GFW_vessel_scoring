import numpy as np
import numpy.lib.recfunctions
import os.path
import math
import scipy.optimize
import matplotlib.pyplot
import sys
import graph_score
import graph_precall
from utils import *

def load_dataset(path, size = 20000):
    # Load a dataset and extract a train, cross validation and test dataset
    #
    # * We need roughly the same amount of fishing and non-fishing
    #   rows to get good predictions, but the source data for some
    #   vessel types contain mostly non-fishing rows, so we randomly
    #   select 1000 fishing rows and the same number of non-fishing
    #   rows
    # * We add the log of the stddev columns, since their values are
    #   exponentially distributed

    x = np.load(path)['x']
    x = np.concatenate((fishy(x)[:size/2], nonfishy(x)[:size/2]))
    np.random.shuffle(x)

    all_windows = get_windows(x)

    for window in all_windows:
        x = np.lib.recfunctions.append_fields(x, 'measure_speedstddev_%s_log' % window, [], dtypes='<f8', fill_value=0.0)
        x['measure_speedstddev_%s_log' % window] = np.log10(x['measure_speedstddev_%s' % window]+0.001)

        x = np.lib.recfunctions.append_fields(x, 'measure_coursestddev_%s_log' % window, [], dtypes='<f8', fill_value=0.0)
        x['measure_coursestddev_%s_log' % window] = np.log10(x['measure_coursestddev_%s' % window]+0.001)


    x = np.lib.recfunctions.append_fields(x, 'score', [], dtypes='<f8', fill_value=0.0)

    length = x.shape[0]
    xtrain = x[:length / 2]
    xcross = x[length/2:length*3/4]
    xtest = x[length*3/4:]

    return xtrain, xcross, xtest
