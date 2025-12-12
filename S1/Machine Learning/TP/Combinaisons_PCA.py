from sklearn import datasets
from sklearn.decomposition import PCA

data = datasets.load_breast_cancer()
X, Y = data.data, data.target
print("Examples = ", X.shape,"Labels = ")