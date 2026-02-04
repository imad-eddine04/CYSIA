import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import svm

df = pd.read_csv("C:/Users/T14s/Desktop/CYSIA/S1/Machine Learning/TP/breast_cancer.csv")
df_copy = df.copy()

print(df_copy.shape)
print(df_copy.info())

print("------------------------------------------------------------------------------")

print(df_copy.head(10))
print("------------------------------------------------------------------------------")

print(df_copy.columns)

#droping the empty columns
print("-------------------#droping the empty columns-----------------------------------------------------------")

df_copy.drop(columns=['Unnamed: 32'], inplace=True)
print(df_copy.head(10))
print(df_copy.columns)

print("-------------------#Replace diagnosis to the last column + transform object into 0 & 1-----------------------------------------------------------")

diagnosis_col = df_copy.pop('diagnosis')
df_copy['diagnosis'] = diagnosis_col

diagnosis_col = df_copy.pop('diagnosis')
df_copy['diagnosis'] = diagnosis_col

df_copy['diagnosis'] = df_copy['diagnosis'].replace({'M': 1, 'B': 0})

print("DataFrame after moving and transforming the 'diagnosis' column:")
print(df_copy.head())
print("\nColumns of the DataFrame:")
print(df_copy.columns)

#show plot
df_copy['diagnosis'].value_counts().plot.bar(title="diagnosis")
plt.show()
print("-------------------#Show duplicated row-----------------------------------------------------------")


duplicate_row = df.duplicated()
print(duplicate_row)

print("-------------------#Show outliers-----------------------------------------------------------")


sns.boxplot(x = "diagnosis", y = "radius_mean", data = df_copy)
plt.show()


X = df_copy.drop(['diagnosis'], axis = 1).values
y = df_copy['diagnosis'].values

print("X : ",X.shape,"y : ",y.shape)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 100, stratify = y)

print("x_train : ",x_train.shape, "y_train : ",y_train.shape)
print("x_test : ",x_test.shape, "y_test : ",y_test.shape)


classifier = svm.SVC(kernel = "linear")

classifier.fit(x_train, y_train)

predicted = classifier.predict(x_test)


print("Classifier Repport : ")
print()


#travaille : svm ydir hyperplane lazm n affichoh