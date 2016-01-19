import numpy

x = numpy.load("classified-filtered.npz")['x']
def fishy(x):
    return x[x["classification"] > 0.5]
def nonfishy(x):
    return x[x["classification"] < 0.5]
xfishy = fishy(x)
xnonfishy = nonfishy(x)
