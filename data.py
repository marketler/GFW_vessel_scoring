import numpy

# Load all the data
x = numpy.genfromtxt(
    "classification_vs_measures.csv",
    delimiter=",",
    names=True,
    missing_values=[""],
    filling_values=[0.0])
def fishy(x):
    return x[x["classification"] > 0.5]
def nonfishy(x):
    return x[x["classification"] < 0.5]
xfishy = fishy(x)
xnonfishy = nonfishy(x)
