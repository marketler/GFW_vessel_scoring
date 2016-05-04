# Find the root directory of vessel-scoring, if running directly from git
import sys, os.path; sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import vessel_scoring.add_measures
import numpy

unscaled_map = {
    'kristina_longliner.npz' : [224068000, 224098250, 224108130],
}

name = os.path.basename(sys.argv[1])
unscaled = unscaled_map.get(name, [])
if unscaled:
    print "NOTE: rescaling MMSI:", unscaled

numpy.savez_compressed(
    sys.argv[2],
    x=vessel_scoring.add_measures.add_measures(
        numpy.load(sys.argv[1])['x'],
        verbose=True,
        unscaled=unscaled,
        err=sys.stderr))
