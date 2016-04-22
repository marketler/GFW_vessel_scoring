import numpy as np
from sklearn.linear_model import LogisticRegression
from utils import get_polynomial_cols



class LogisticModel(LogisticRegression):

    # TODO: see what the correct way to write init's for sklearn is
    def __init__(self, order=4, cross=0, windows=['3600'],
                    random_state=4321, **kwargs):
        """
        order - maximum order of polynomial terms
        cross - maximum order of cross terms (2 is minimum for any effect)
        windows - list of window sizes to use in features

        Note that this uses only cross terms from two features at
        a time.
        """
        LogisticRegression.__init__(self, random_state=random_state,
                                     **kwargs)
        assert order >= 2, "order must be at least 2"
        self.order = order
        self.cross = cross
        self.windows = windows

    def make_features(self, data):
        """Convert dataset into feature matrix suitable for model"""
        base = np.array(get_polynomial_cols(data, self.windows))
        n_base_cols = len(base)
        cols = []
        for total_order in range(1, self.order+1):
            for i in range(n_base_cols):
                cols.append(base[i]**total_order)
            if total_order <= self.cross:
                for i in range(n_base_cols):
                    for j in range(i+1, n_base_cols):
                        # Loop from i+1 up, so that we only get
                        # off diagonal terms once.
                        for sub_order in range(1, total_order):
                            # sub_order ranges from 1-total_order-1
                            # so only when i==j do we get columns
                            # with total order.
                            cols.append(base[i] ** sub_order *
                                        base[j] ** (total_order - sub_order))
        chunks = [x.reshape(-1,1) for x in cols]
        return np.concatenate(chunks, axis=1)