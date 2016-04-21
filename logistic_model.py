import numpy as np
from sklearn.linear_model import LogisticRegression
from utils import get_polynomial_cols


class LogisticModel(LogisticRegression):

    @staticmethod
    def make_features(data, order=5, windows=['3600']):
        base = np.array(get_polynomial_cols(data, windows)).transpose()
        return np.concatenate([base**i for i in range(1, order+1)], axis=1)
