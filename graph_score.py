from matplotlib.pyplot import *
from numpy import *
from utils import *

def graph_score(x, col):
    xfishy = fishy(x)
    xnonfishy = nonfishy(x)

    histfig = figure(figsize=(20,5))
    subplot = histfig.add_subplot(111)
    new_score_fishy = subplot.hist(xfishy[col], bins=200, normed=False, color='b', alpha=0.5, label="fishy score")
    new_score_nonfishy = subplot.hist(xnonfishy[col], bins=200, normed=False, color='r', alpha=0.5, label="nonfishy score")
    legend()
    show()

    xclassified = x[x["classification"] != Inf]
    print "Squared numerical error: %s" % (sum((xclassified[col] - xclassified['classification'])**2)/xclassified.shape[0])

    total = sum(new_score_fishy[0] + new_score_nonfishy[0])
    non_overlap = sum(abs(new_score_fishy[0] - new_score_nonfishy[0]))
    overlap = total - non_overlap
    error = overlap / total

    print "Error (overlap): %s%%" % (error * 100)

    cutoff = len(new_score_fishy[1][new_score_fishy[1] < 0.5])
    total = sum(new_score_fishy[0][cutoff:] + new_score_nonfishy[0][cutoff:])
    non_overlap = sum(abs(new_score_fishy[0][cutoff:] - new_score_nonfishy[0][cutoff:]))
    overlap = total - non_overlap
    error = overlap / total

    print "False positives given cutoff at 0.5: %s%%" % (error * 100)
