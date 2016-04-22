import numpy as np
from sklearn.ensemble import RandomForestClassifier
from utils import get_polynomial_cols


class RandomForestModel(RandomForestClassifier):
    def __init__(self, windows=['3600'], random_state=4321,
                        n_estimators=200, **kwargs):
        RandomForestClassifier.__init__(self,
                                        n_estimators=n_estimators,
                                        random_state=random_state,
                                        **kwargs)
        self.windows = windows

    def make_features(self, data):
        return  np.transpose(get_polynomial_cols(data, self.windows))

