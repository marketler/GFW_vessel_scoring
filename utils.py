import numpy as np
import os.path
import math
import scipy.optimize

# Define some usefull functions
def clamp(x, low, high):
    return np.where(x <= high,
        np.where(x >= low, x, low),
        high)

def center_hist_bins(histres):
    y = histres[0]
    x = histres[1]
    x = (x[:-1] + x[1:]) / 2.0
    return y, x

def polynomial(x, *args):
    res = 0
    for ind, arg in enumerate(args):
        res += arg * x**ind
    return res

def linear(x, *args):
    res = 0.0
    for idx, arg in enumerate(args):
        res += x[idx]*arg
    return res

def mpolynomial(x, *args):
    res = 0
    for col, colargs in zip(x, np.array_split(args, len(x))):
        res += polynomial(col, *colargs)
    return res

def zigmoid(z):
    z = np.where(z < -100, -100, z)
    return 1. / (1. + np.exp(-z))

def zmpolynomial(x, *args):
    return zigmoid(mpolynomial(x, *args))

def cached(path):
    def cached(fn):
        def cached(*arg, **kw):
            if os.path.exists(path):
                return np.load(path)['cached']
            else:
                res = fn(*arg, **kw)
                np.savez_compressed(path, cached = res)
                return res
        return cached
    return cached

def fishy(x):
    return x[x["classification"] >= 0.5]
def nonfishy(x):
    return x[x["classification"] < 0.5]


def get_polynomial_cols(x, windows):
    colnames = []
    #colnames.append("speed")
    for window in windows:
        colnames.append('measure_speedavg_%s' % window)
        colnames.append('measure_speedstddev_%s_log' % window)
        colnames.append('measure_coursestddev_%s_log' % window)

    cols = [x[col] for col in colnames]

    return cols

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
