from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets, linear_model
from sklearn import metrics
import numpy as np
from sklearn.datasets import fetch_california_housing
dat = fetch_california_housing()
X = dat.data
Y = dat.target


print("Examples = ",X.shape ," Labels = ", Y.shape)
fig, ax = plt.subplots(figsize=(12,8))
ax.scatter(X[:,0], Y, edgecolors=(0, 0, 0))
ax.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'k--', lw=4)
ax.set_xlabel('F')
ax.set_ylabel('Y')
plt.show()

fig1 = plt.figure(figsize=(12, 8))
ax = fig1.add_subplot(111, projection='3d')
ax.scatter(X[:, 0], X[:, 1], Y,
           c='b', marker='o',
           edgecolor='k', s=40)
ax.set_title("My Data")
ax.set_xlabel("F1")
ax.xaxis.set_ticklabels([])
ax.set_ylabel("F2")
ax.yaxis.set_ticklabels([])
ax.set_zlabel("Y")
ax.zaxis.set_ticklabels([])
plt.show()

X_train, X_test, Y_train, Y_test = train_test_split(X,
Y, test_size= 0.20, random_state=100)
print("X_train = ",X_train.shape ," Y_test = ", Y_test.shape)
regressor = linear_model.LinearRegression()
regressor.fit(X_train, Y_train)
predicted = regressor.predict(X_test)


import pandas as pd
df = pd.DataFrame({'Actual': Y_test.flatten(), 'Predicted': predicted.flatten()})
print(df)
df1 = df.head(25)
df1.plot(kind='bar',figsize=(12,8))
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.show()

predicted_all = regressor.predict(X)
fig2, ax = plt.subplots(figsize=(12,8))
ax.scatter(X[:,0], Y, edgecolors=(0, 0, 1))
ax.scatter(X[:,0], predicted_all, edgecolors=(1, 0, 0))
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:, 0], X[:, 1], Y, c='b', marker='o', edgecolor='k', s=40)
ax.scatter(X[:, 0], X[:, 1], predicted_all, c='r', marker='o', edgecolor='k',
s=40)
ax.set_title("My Data")
ax.set_xlabel("F1")
ax.xaxis.set_ticklabels([])
ax.set_ylabel("F2")
ax.yaxis.set_ticklabels([])
ax.set_zlabel("Y")
ax.zaxis.set_ticklabels([])
plt.show()


print('Mean Absolute Error : ', metrics.mean_absolute_error(Y_test, predicted))
print('Mean Squared Error : ', metrics.mean_squared_error(Y_test, predicted))
print('Root Mean Squared Error: ', np.sqrt(metrics.mean_squared_error(Y_test, predicted)))