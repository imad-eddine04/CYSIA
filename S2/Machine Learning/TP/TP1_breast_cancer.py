import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import svm
from sklearn.decomposition import PCA

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


print("--- Original Model Trained on 30 Features ---")
print("x_train shape:", x_train.shape, "y_train shape:", y_train.shape)
print("x_test shape:", x_test.shape, "y_test shape:", y_test.shape)
print("\nPrediction results from original model (first 10):", predicted[:10])
print("---------------------------------------------------\n")


# --- NEW SECTION: PCA and Hyperplane Visualization ---

print("--- Visualizing SVM Hyperplane with PCA ---")

# 1. Reduce data to 2 dimensions using PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# 2. Train a new SVM classifier on the 2D data
classifier_2d = svm.SVC(kernel="linear")
classifier_2d.fit(X_pca, y)

# 3. Create a mesh grid to plot the decision boundary
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Create grid to evaluate model
xx = np.linspace(X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1, 30)
yy = np.linspace(X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1, 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = classifier_2d.decision_function(xy).reshape(XX.shape)

# 4. Plot the decision boundary and margins
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])

# Highlight the support vectors
ax.scatter(classifier_2d.support_vectors_[:, 0], classifier_2d.support_vectors_[:, 1], s=100,
           linewidth=1, facecolors='none', edgecolors='k', label='Support Vectors')

# 5. Plot the 2D data points
scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap=plt.cm.coolwarm, s=30, label='Data Points')

# Add labels and title
plt.xlabel("First Principal Component")
plt.ylabel("Second Principal Component")
plt.title("SVM Hyperplane on 2D PCA Data")
plt.legend()
plt.show()


#travaille : svm ydir hyperplane lazm n affichoh


