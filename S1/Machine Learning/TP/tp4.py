from sklearn import datasets
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics



iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names
print("Feature names:", feature_names)
print("Target names:", target_names)



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state =1)
print("X_train.shape: ", X_train.shape)
print("X_test.shape : ", X_test.shape)
print("y_train.shape:", y_train.shape)
print("y_test.shape:", y_test.shape)


model = SVC()
model.fit(X_train,y_train)



y_predict = model.predict(X_test)
exactitude = metrics.accuracy_score(y_test, y_predict)
print("Accuracy = ", exactitude)
f_score = metrics.f1_score(y_test, y_predict, average="macro")
print("F1-score", f_score)
precision = metrics.precision_score(y_test, y_predict, average="macro")
print("Précision = ", precision)
rappel = metrics.recall_score(y_test, y_predict, average="macro")
print("Rappel = ", rappel)




"""""
test_mean = df['Test Score'].mean()

# 2. Fill the missing values (NaN) in 'Test Score' with the calculated mean
df['Test Score'] = df['Test Score'].fillna(test_mean)

# 3. Fill the missing values in 'Height(m)' with its mean
height_mean = df['Height(m)'].mean()
df['Height(m)'] = df['Height(m)'].fillna(height_mean)

# After imputation, the DataFrame has no NaN values:
print("\nDataFrame after Imputation:\n", df)
print("\nFinal SUM of NaNs:\n", df.isnull().sum())

"""""