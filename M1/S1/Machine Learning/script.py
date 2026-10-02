from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import numpy as np

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
print(X_train)

quantile_transformer = preprocessing.QuantileTransformer(random_state=0)
X_train_trans = quantile_transformer.fit_transform(X_train)
print(X_train_trans)

X_test_trans = quantile_transformer.transform(X_test)

# Compute the q-th percentile of the data along the specified axis.
np.percentile(X_train[:, 0], [0, 25, 50, 75, 100])
