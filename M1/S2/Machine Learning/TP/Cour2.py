import numpy as np
import seaborn as sns
import pandas as pd
from sklearn import datasets, metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


from sklearn.metrics import RocCurveDisplay
from sklearn.decomposition import PCA

# 1. Load the dataset
# Note: I'm loading from sklearn and creating a DataFrame to match your logic
dat = datasets.load_breast_cancer()
df = pd.DataFrame(data=dat.data, columns=dat.feature_names)
df['diagnosis'] = dat.target

# If you want to use your local CSV, uncomment the line below:
# df = pd.read_csv("breast_cancer.csv")

df_copy = df.copy()

print("Shape:", df_copy.shape)
print("\nInfo:")
print(df_copy.info())

print("-" * 30)
print(df_copy.head(10))
print("-" * 30)

# 2. Dropping empty columns (e.g., Unnamed: 32 often found in Kaggle datasets)
if 'Unnamed: 32' in df_copy.columns:
    df_copy.drop(columns=['Unnamed: 32'], inplace=True)
    print("Dropped 'Unnamed: 32'")

# 3. Move 'diagnosis' to the last column
# If loading from sklearn directly, it's already 0/1.
# If loading from CSV where it is 'M'/'B', the replace logic below handles it.
if df_copy['diagnosis'].dtype == 'object':
    df_copy['diagnosis'] = df_copy['diagnosis'].replace({'M': 1, 'B': 0})

diagnosis_col = df_copy.pop('diagnosis')
df_copy['diagnosis'] = diagnosis_col

print("\nDataFrame after moving/transforming 'diagnosis':")
print(df_copy.head())

# 4. Show plot
df_copy['diagnosis'].value_counts().plot.bar(title="Diagnosis Count (0: Benign, 1: Malignant)")
plt.show()

# 5. Show duplicated rows
print("-" * 30)
print("Duplicate rows count:", df_copy.duplicated().sum())

# 6. Show outliers using the DataFrame (df_copy)
# We use one of the feature names, e.g., 'mean radius'
feature_to_plot = 'mean radius' if 'mean radius' in df_copy.columns else df_copy.columns[0]
sns.boxplot(x="diagnosis", y=feature_to_plot, data=df_copy)
plt.title(f"Boxplot of {feature_to_plot} by Diagnosis")
plt.show()

# 7. Model Training
# Prepare X (features) and y (target) from the DataFrame
X = df_copy.drop(['diagnosis'], axis=1).values
y = df_copy['diagnosis'].values

print(f"Features shape: {X.shape}, Labels shape: {y.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression
logreg = LogisticRegression(max_iter=10000) # Increased iterations for convergence
logreg.fit(X_train, y_train)
predicted = logreg.predict(X_test)

# 8. Classification Report
print("\nClassification report for classifier:\n", classification_report(y_test, predicted))

# 9. Confusion Matrix
disp = ConfusionMatrixDisplay.from_estimator(logreg, X_test, y_test, cmap=plt.cm.Blues)
disp.ax_.set_title("Confusion Matrix for Logistic Regression")
plt.show()


# --- Added Section: Classification Visualizations ---

# 1. ROC Curve
# This shows the performance of the binary classifier
RocCurveDisplay.from_estimator(logreg, X_test, y_test)
plt.title("ROC Curve for Logistic Regression")
# FIX: Changed 'style' to 'linestyle'
plt.grid(linestyle='--', alpha=0.5)
plt.show()

# 2. PCA Visualization of the Classification
# Since the data has 30 features, we use PCA to reduce it to 2D for plotting
pca = PCA(n_components=2)
X_test_2d = pca.fit_transform(X_test)

plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_test_2d[:, 0], X_test_2d[:, 1], c=predicted, cmap='RdYlBu', edgecolor='k', alpha=0.8)
plt.title("Classification Results in 2D (PCA Projection)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(handles=scatter.legend_elements()[0], labels=['Benign (0)', 'Malignant (1)'], title="Predictions")
plt.show()

# nkemlo le graph li yprizonti la classification de regression