
# 7. Clustering - K-means

import matplotlib.pyplot as plt
import seaborn as sns; sns.set() # for plot styling
import numpy as np
from sklearn.datasets import make_blobs
# n_features=1, optional (default=2)
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=1.5, random_state=100)
print("Example = ", X.shape)

# Visualize the Data
fig, ax = plt.subplots(figsize=(8,5))
ax.scatter(X[:, 0], X[:, 1], s=50)
ax.set_title("Visualize the Data")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show()


from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)
print("the 4centroids that the algorithm found : /n",kmeans.cluster_centers_)

#Visualisation the results
fig, ax = plt.subplots(figsize=(8,5))
ax.scatter(X[:, 0], X[:, 1],c = y_kmeans , s=50, cmap='viridis')
centers = kmeans.cluster_centers_
ax.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
ax.set_title("K-means Clustering Results")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show()

#Assign new instances to the cluster whose centroid is closet:
X_new = np.array([[0,2],[3,2],[-3,3],[-3,2.5]])

y_kmeans_new = kmeans.predict(X_new)

#The transform() method measures the distance from each istance to every centroid:

print("The distance from each instance to every centroid: /n",kmeans.transform(X_new))
#Visualize the new results

fig, ax= plt.subplots(figsize=(8,5))

ax.scatter(X_new[:,0],X_new[:,1],c=y_kmeans_new,cmap='viridis')

centers = kmeans.cluster_centers_

ax.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
ax.set_title("Visualize the new Results")

ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show()

''''
# Create Clusters
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=10)
y_kmeans = kmeans.fit_predict(X)

# Visualize the Clusters
fig, ax = plt.subplots(figsize=(8,5))
ax.scatter(X[:, 0], X[:, 1], c=y_kmeans, cmap='viridis')
ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
           marker='x', s=200, linewidths=3, color='red', label='Centroids')
ax.set_title("K-means Clustering Results")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()
plt.show()
'''