import numpy
import os.path

# Define some usefull functions
def clamp(x, low, high):
    return numpy.where(x <= high,
        numpy.where(x >= low, x, low),
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
    for col, colargs in zip(x, numpy.array_split(args, len(x))):
        res += polynomial(col, *colargs)
    return res

def cached(path):
    def cached(fn):
        def cached(*arg, **kw):
            if os.path.exists(path):
                return numpy.load(path)['cached']
            else:
                res = fn(*arg, **kw)
                numpy.savez_compressed(path, cached = res)
                return res
        return cached
    return cached

def fishy(x):
    return x[x["classification"] >= 0.5]
def nonfishy(x):
    return x[x["classification"] < 0.5]
