from sklearn import datasets
from sklearn.decomposition import KernelPCA

data = datasets.load_breast_cancer()
X, Y = data.data, data.target
print("Examples = ",X.shape,"Labels = ",Y.shape)

kpca = KernelPCA(n_=7, kernel='rbf')