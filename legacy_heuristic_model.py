import numpy as np
from utils import make_simple_features

COURSE_STD = 0
SPEED_STD = 1
SPEED_AVG = 2
SHORE_DIST = 3

# TODO: make this inherit from appropriate sklearn lasses
class LegacyHeuristicModel:

    def fit(self, X, y):
        return self

    def predict_proba(self, X):
        score = (X[:,COURSE_STD] + X[:,SPEED_STD] + X[:,SPEED_AVG]) * 2.0 / 3.0
        score = np.clip(score, 0, 1)
        # Port behavior is hard to distinguish from fishing,
        # so supress score close to shore...
#         not_close_to_shore = X[:,SHORE_DIST] >= 3
#         score *= not_close_to_shore
        proba = np.zeros([len(X), 2])
        proba[:, 0] = 1 - score # Probability not fishing
        proba[:, 1] = score
        return proba

    @staticmethod
    def make_features(data, window='3600'):
          return make_simple_features(data, ['measure_coursestddev_{window}',
                                             'measure_speedstddev_{window}',
                                             'measure_speedavg_{window}',
            #                                'distance_to_shore' # XXX waiting for this feature to be re-added
                                             ], window=window)