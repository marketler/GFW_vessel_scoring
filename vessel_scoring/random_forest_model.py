import numpy as np
from sklearn.ensemble import RandomForestClassifier
from vessel_scoring.utils import get_polynomial_cols
import vessel_scoring.base_model

class RandomForestModel(RandomForestClassifier, vessel_scoring.base_model.BaseModel):

    def __init__(self, windows=['3600'], random_state=4321,
                        n_estimators=200):
        """
        windows - list of window sizes to use in features
        See RandomForestClassifier docs for other parameters.
        """
        RandomForestClassifier.__init__(self,
                                        n_estimators=n_estimators,
                                        random_state=random_state)
        self.windows = windows

    def predict_proba(self, X):
        X = np.transpose(get_polynomial_cols(X, self.windows))
        return RandomForestClassifier.predict_proba(self, X)

    def fit(self, X, y):
        X = np.transpose(get_polynomial_cols(X, self.windows))
        return RandomForestClassifier.fit(self, X, y)


