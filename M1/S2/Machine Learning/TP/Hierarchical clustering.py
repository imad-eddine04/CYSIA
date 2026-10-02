import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from sklearn.neighbors import KNeighborsClassifier


def plot_dendrogram(model, **kwargs):
    """
    This function creates the linkage matrix and then plots the dendrogram.
    It's a helper function necessary for visualizing the clustering hierarchy.
    """
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_, counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

# --- Start of your original code structure ---

X = np.array([[5,3], [10,15], [15,12], [24,10], [30,30], [85,70], [71,80], [60,78], [70,55], [80,91],])

# To plot a dendrogram, distance_threshold must be used and n_clusters must be None.
# The model also needs to compute the full tree for the dendrogram.
# Setting distance_threshold=0 forces all points to be in their own cluster.
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None, compute_full_tree=True)
model.fit(X)

print("---------------------------------------------------------")
# With distance_threshold=0, every point is its own cluster.
print(f"Number of clusters found: {model.n_clusters_}")
print(f"Number of connected components: {model.n_connected_components_}")
print("-------------------------------------------------------------")

cluster_model = AgglomerativeClustering(n_clusters=2)
cluster_labels = cluster_model.fit_predict(X)
print(f"Original Data:\n{X}")
print(f"Cluster Labels from AgglomerativeClustering:\n{cluster_labels}\n")

# 2. Train a supervised classifier on the cluster results
# We use the original data as features and the cluster labels as targets
classifier = KNeighborsClassifier(n_neighbors=3)
classifier.fit(X, cluster_labels)

# 3. Predict the cluster for your new point
new_point = np.array([[35, 45]])
predicted_cluster = classifier.predict(new_point)

print("-----------------------------------------")
print(f"New data point: {new_point[0]}")
print(f"Predicted cluster for the new point: {predicted_cluster[0]}")
print("-----------------------------------------")

plt.figure(figsize=(10, 7))
plt.title("Hierarchical Clustering Dendrogram")
# Plot the top levels of the dendrogram
plot_dendrogram(model, truncate_mode="level", p=3)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()
