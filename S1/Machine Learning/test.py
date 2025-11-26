import numpy as np
from sklearn.preprocessing import StandardScaler

X_train = np.array([[1.,-1.,2],
                    [2.,0.,0],
                    [0.,1.,-1]])
scaler = StandardScaler().fit_transform(X_train)
print(scaler)