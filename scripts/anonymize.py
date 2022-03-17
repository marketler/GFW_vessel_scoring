#! /usr/bin/env python

# Usage: anonymize.py PASSWORD INFILE OUTFILE

import numpy as np
import sys
import hashlib

x = np.load(sys.argv[2])['x']

for mmsi in np.unique(x['mmsi']):
    print mmsi
    h = hashlib.sha1()
    h.update(sys.argv[1])
    h.update(str(mmsi))
    hashmmsi = int(h.hexdigest()[:12], 16)

    x['mmsi'][x['mmsi'] == mmsi] = hashmmsi

np.savez(sys.argv[3], x=x)

