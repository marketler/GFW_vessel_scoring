import csv
from numpy import *
from scipy.optimize import *
from numpy.lib.recfunctions import *
from utils import *
from data import *

for window in (1800,3600,10800,21600,43200,86400):
    print "Window: %s" % window

    new_score_fishy = histogram(xfishy["measure_new_score_%s" % window][xfishy['distance_to_shore'] > 3], bins=200, normed=False)
    new_score_nonfishy = histogram(xnonfishy["measure_new_score_%s" % window][xnonfishy['distance_to_shore'] > 3], bins=200, normed=False)

    total = float(sum(new_score_fishy[0] + new_score_nonfishy[0]))
    non_overlap = float(sum(abs(new_score_fishy[0] - new_score_nonfishy[0])))
    overlap = total - non_overlap
    error = overlap / total

    print "    Error for measure_new_score: %s%%" % (error * 100)

    cutoff = float(len(new_score_fishy[1][new_score_fishy[1] < 0.5]))
    total = float(sum(new_score_fishy[0][cutoff:] + new_score_nonfishy[0][cutoff:]))
    non_overlap = float(sum(abs(new_score_fishy[0][cutoff:] - new_score_nonfishy[0][cutoff:])))
    overlap = total - non_overlap
    error = overlap / total

    print "    False positives for measure_new_score: %s%%" % (error * 100)
