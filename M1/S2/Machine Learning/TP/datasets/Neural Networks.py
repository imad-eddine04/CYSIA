import pandas as pd
from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

# 1. Load the dataset from your path
path = "breast_cancer.csv"
df = pd.read_csv(path)

# Preprocessing (Mapping labels and dropping unnecessary columns as shown in sources)
df.drop(df.columns[[-1, 0]], axis=1, inplace=True)
df['diagnosis'] = df['diagnosis'].map({'B': 0, 'M': 1})
X = df.drop(["diagnosis"], axis=1).values
y = df["diagnosis"].values

# 2. Training and Test Sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=100, stratify=y
)

# 3. Feature Scaling (Exactly as shown on page 153)
scaler = StandardScaler()
scaler.fit(X_train)
X_trainNN = scaler.transform(X_train)
X_testNN = scaler.transform(X_test)

# 4. Training and Predictions (Using parameters from page 153 screenshot)
mlp = MLPClassifier(
    hidden_layer_sizes=(100, 100,),
    batch_size=128,
    solver="lbfgs",
    alpha=0.1,
    activation="logistic",
    max_iter=10000,
    random_state=42
)
mlp.fit(X_trainNN, y_train)

# 5. Evaluation (Updated for modern scikit-learn versions)
predicted = mlp.predict(X_testNN)

# Comparing actual response values with predicted response values
print("Classification report : \n", metrics.classification_report(y_test, predicted))

# Plot Confusion Matrix using the modern replacement for plot_confusion_matrix
disp = metrics.ConfusionMatrixDisplay.from_estimator(mlp, X_testNN, y_test)
disp.figure_.suptitle("Confusion Matrix")

# To print the numeric matrix as shown on page 153
print("Confusion matrix: \n", disp.confusion_matrix)
plt.show()

import time

# ... [after model training] ...

# 6. Measure Classification Time
start_time = time.time()
predicted = mlp.predict(X_testNN)
end_time = time.time()

classification_time = end_time - start_time
print(f"Classification time: {classification_time:.6f} seconds")

# ... [continue with evaluation metrics like classification_report] ...