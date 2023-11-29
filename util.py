import numpy as np
from pyod.utils.data import generate_data

def inv_stereo(X):
    n = len(X[0])
    m = len(X)
    new_X = []
    for j in range(m):
        s = sum(X[j]**2)
        for i in range(n):
            X[j][i] = 2*X[j][i]
        new_X.append([x for x in X[j]])
        new_X[j] = np.append(X[j], np.array(s-1))
        new_X[j] = new_X[j]/(s+1)
    return new_X



def generate_dataset(M, N, t):
    X_train, Y_train = generate_data(n_train=M, n_features=N, train_only=True, contamination=0.3, random_state=t*13)
    return X_train 