from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import tree
# New import for the confusion matrix plot
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt # Often needed to display plots

# Load the iris dataset
dat = load_iris()
# Store the feature matrix (X) and response vector (y)
X = dat.data
y = dat.target

# Splitting X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

# Training the model on the training set
# You can be explicit with the hyperparameters if you want
tree_clf = DecisionTreeClassifier(max_depth=2, criterion='gini', random_state=100)
tree_clf.fit(X_train, y_train)

# Making predictions on the testing set
predicted = tree_clf.predict(X_test)

# Comparing actual response values (y_test) with predicted response values (predicted)
print("Classification report:")
print(metrics.classification_report(y_test, predicted))

# --- CORRECTED PART ---
# The old `plot_confusion_matrix` is replaced by `ConfusionMatrixDisplay.from_estimator`
print("Generating Confusion Matrix...")
disp = ConfusionMatrixDisplay.from_estimator(tree_clf, X_test, y_test)
disp.figure_.suptitle("Confusion Matrix")
print("Confusion matrix:\n", disp.confusion_matrix)

# Show the plot
plt.show()

# --- PLOT THE TREE ---
# Plot the tree with the plot_tree function (pass the already fitted classifier)
print("Generating Decision Tree Plot...")
plt.figure(figsize=(12,8)) # You can adjust the figure size to make the tree more readable
tree.plot_tree(tree_clf,
               feature_names=dat.feature_names,
               class_names=dat.target_names,
               filled=True)
plt.show()


print("predict_proba : ",tree_clf.predict_proba([[1, 1.5, 3.2, 0.5]]))


# To get the label directly
prediction_label = tree_clf.predict([[1, 1.5, 3.2, 0.5]])
# The output will be an array with the class index
print("Predicted class index:", prediction_label) # This will print [1]

# To get the actual name
predicted_class_name = dat.target_names[prediction_label[0]]
print("Predicted class name:", predicted_class_name) # This will print 'versicolor'
