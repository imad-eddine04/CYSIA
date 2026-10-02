import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons

# Generate the two moons dataset
X, y = make_moons(n_samples=1000, noise=0.1, random_state=42)

# Your provided code for applying DBSCAN
dbscan = DBSCAN(eps=0.05, min_samples=5)
dbscan.fit(X)

print("the label of all the instance",dbscan.labels_,"/n")

print("the indice of the core instance", len(dbscan.core_sample_indices_),"/n",dbscan.core_sample_indices_)

print("the core instance",dbscan.components_,"/n",dbscan.components_)

# Visualize the results
plt.figure(figsize=(8, 5))
# We color the points based on the labels found by DBSCAN
plt.scatter(X[:, 0], X[:, 1], c=dbscan.labels_, cmap='viridis', s=50)
plt.title("DBSCAN Clustering Results")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()