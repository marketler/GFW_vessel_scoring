#! /bin/env python

import numpy

# Load all the data
x = numpy.genfromtxt(
    "classified-filtered.csv",
    delimiter=",",
    names=True,
    missing_values=[""],
    filling_values=[0.0])

numpy.savez_compressed(
    "classified-filtered.npz",
    x=x)
