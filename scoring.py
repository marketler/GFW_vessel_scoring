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

def fit_score(x, windows, grade=4, lambda_val=0.0001):
    # A pretty straight-forward implementation of regularized
    # logistical regression without an analytical gradient...

    cols = get_polynomial_cols(x, windows)
    y = x['classification']
    m = float(y.shape[0])

    def objective(theta):
        h = zmpolynomial(cols, *theta)

        a = -y*np.log(np.where(h == 0., 1e-100, h))
        a = np.where(y == 0., 0., a)
        b = -(1. - y)*np.log(np.where(h == 1., 1e-100, 1. - h))
        b = np.where(y == 1., 0., b)

        J = np.sum(a + b) / m
        Jreg = J + lambda_val * np.sum(theta**2) / (2 * m)
        return Jreg
  
    return scipy.optimize.minimize(objective, [1]*(len(cols)*grade)).x

    # return curve_fit(
    #     zmpolynomial,
    #     cols,
    #     x['classification'],
    #     [1]*(len(cols)*grade))[0]

def optimize_window_size(xtrain, xcross, grade = 4):
    print "Fitting an optimal window size for avg/stddev columns"

    windows = np.array(get_windows(xtrain))
    err_train = np.zeros(windows.shape[0])
    err_cross = np.zeros(windows.shape[0])

    for idx, window in enumerate(windows):
        print "%s: Fitting..." % window,
        sys.stdout.flush()
        score_args = fit_score(xtrain, [window], grade)
        print "Scoring...",
        sys.stdout.flush()
        xtrain['score'][:] = zmpolynomial(get_polynomial_cols(xtrain, [window]), *score_args)
        xcross['score'][:] = zmpolynomial(get_polynomial_cols(xcross, [window]), *score_args)

        print "Calc.err...",
        sys.stdout.flush()
        xtrainclassified = xtrain[xtrain["classification"] != np.Inf]
        err_train[idx] = np.sum((xtrainclassified['score'] - xtrainclassified['classification'])**2)/xtrainclassified.shape[0]
        xcrossclassified = xcross[xcross["classification"] != np.Inf]
        err_cross[idx] = np.sum((xcrossclassified['score'] - xcrossclassified['classification'])**2)/xcrossclassified.shape[0]
        print "train=%s, cross=%s" % (err_train[idx], err_cross[idx])
        sys.stdout.flush()

    min_window = windows[np.argmin(err_cross)]

    matplotlib.pyplot.figure(figsize=(20,5))
    matplotlib.pyplot.plot(windows, err_train, label="err train")
    matplotlib.pyplot.plot(windows, err_cross, label="err cross")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.xlabel("Window size in seconds")
    matplotlib.pyplot.show()

    print "Best window size: %s" % min_window

    return min_window

def optimize_polynomial_degree(xtrain, xcross, min_window, max_grade = 10):
    print "Fitting an optimal degree of polynomial"

    windows = [min_window]
    grades = range(2, max_grade)
    err_train = np.zeros(len(grades))
    err_cross = np.zeros(len(grades))

    for idx, grade in enumerate(grades):
        print "%s: Fitting..." % grade,
        sys.stdout.flush()
        score_args = fit_score(xtrain, windows, grade)
        print "Scoring...",
        sys.stdout.flush()
        xtrain['score'][:] = zmpolynomial(get_polynomial_cols(xtrain, windows), *score_args)
        xcross['score'][:] = zmpolynomial(get_polynomial_cols(xcross, windows), *score_args)

        print "Calc.err...",
        sys.stdout.flush()
        xtrainclassified = xtrain[xtrain["classification"] != np.Inf]
        err_train[idx] = np.sum((xtrainclassified['score'] - xtrainclassified['classification'])**2)/xtrainclassified.shape[0]
        xcrossclassified = xcross[xcross["classification"] != np.Inf]
        err_cross[idx] = np.sum((xcrossclassified['score'] - xcrossclassified['classification'])**2)/xcrossclassified.shape[0]
        print "train=%s, cross=%s" % (err_train[idx], err_cross[idx])
        sys.stdout.flush()
    grades = np.array(grades)

    matplotlib.pyplot.figure(figsize=(20,5))
    matplotlib.pyplot.plot(grades, err_train, label="err train")
    matplotlib.pyplot.plot(grades, err_cross, label="err cross")
    matplotlib.pyplot.legend()
    matplotlib.pyplot.xlabel("Polynomial degree (for each variable)")
    matplotlib.pyplot.show()


def evaluate_score(xtrain, xtest, grade, min_window):
    windows = [min_window]
    score_args = fit_score(xtrain, windows, grade)
    xtest['score'][:] = zmpolynomial(get_polynomial_cols(xtest, windows), *score_args)
    graph_score.graph_score(xtest, "score")
    graph_precall.graph_precall(xtest, "score")
    print "Score window:", min_window
    print "Score polynomial:", score_args
