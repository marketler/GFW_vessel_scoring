import numpy as np
from sklearn.ensemble import RandomForestClassifier
from utils import get_polynomial_cols


class RandomForestModel(RandomForestClassifier):
    def __init__(self, random_state=0, n_estimators=200, **kwargs):
        RandomForestClassifier.__init__(self,
                                        n_estimators=n_estimators,
                                        random_state=random_state,
                                        **kwargs)

    @staticmethod
    def make_features(data, windows=['3600']):
        return  np.transpose(get_polynomial_cols(data, windows))

