import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA

# Set style for all plots
sns.set_theme(style="whitegrid")

# -------------------------------------------------------------------------------------------
# --- Step 1: Load the dataset ---
try:
    df = pd.read_csv('Loan.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'Loan.csv' not found. Please ensure the file is in the same directory.")
    exit()

# --- 1. Missing Values Visualization ---
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.show()

# -------------------------------------------------------------------------------------------
# --- Step 2: Outlier Analysis (Before) ---
numerical_cols = ['credit_score', 'annual_income', 'loan_amount', 'employment_duration', 'Age']
existing_cols = [col for col in numerical_cols if col in df.columns]

plt.figure(figsize=(12, 6))
sns.boxplot(data=df[existing_cols])
plt.title('Boxplot Before Outlier Handling')
plt.xticks(rotation=45)
plt.show()

# -------------------------------------------------------------------------------------------
# --- Step 3: Data Cleaning ---
df_copy = df.copy()

# Imputation
for col in numerical_cols:
    if col in df_copy.columns:
        df_copy[col].fillna(df_copy[col].mean(), inplace=True)

# Outlier Handling (Capping)
for col in existing_cols:
    Q1 = df_copy[col].quantile(0.25)
    Q3 = df_copy[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_copy[col] = np.where(df_copy[col] < lower_bound, lower_bound, df_copy[col])
    df_copy[col] = np.where(df_copy[col] > upper_bound, upper_bound, df_copy[col])

# --- 2. Boxplot After Outlier Handling ---
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_copy[existing_cols])
plt.title('Boxplot After Outlier Handling (Capping)')
plt.xticks(rotation=45)
plt.show()

# -------------------------------------------------------------------------------------------
# --- Step 4: Feature Distribution Histograms ---
fig, ax = plt.subplots(1, 3, figsize=(18, 5))

if 'credit_score' in df_copy.columns:
    sns.histplot(df_copy['credit_score'], kde=True, ax=ax[0], color='blue')
    ax[0].set_title('Histogram: Credit Score')
else:
    ax[0].text(0.5, 0.5, 'credit_score not found', ha='center')

if 'annual_income' in df_copy.columns:
    sns.histplot(df_copy['annual_income'], kde=True, ax=ax[1], color='green')
    ax[1].set_title('Histogram: Annual Income')
else:
    ax[1].text(0.5, 0.5, 'annual_income not found', ha='center')

if 'loan_amount' in df_copy.columns:
    sns.histplot(df_copy['loan_amount'], kde=True, ax=ax[2], color='purple')
    ax[2].set_title('Histogram: Loan Amount')
else:
    ax[2].text(0.5, 0.5, 'loan_amount not found', ha='center')

plt.tight_layout()
plt.show()

# -------------------------------------------------------------------------------------------
# --- Step 5: Correlation Matrix & Scatterplot ---
plt.figure(figsize=(10, 8))
corr = df_copy[existing_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()

if 'credit_score' in df_copy.columns and 'annual_income' in df_copy.columns:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_copy, x='credit_score', y='annual_income', hue='default', alpha=0.6)
    plt.title('Scatterplot: Credit Score vs Annual Income')
    plt.show()

# -------------------------------------------------------------------------------------------
# --- Step 6: Encoding & Scaling ---
if 'Vehicle_Ownership' in df_copy.columns:
    df_copy['Vehicle_Ownership'] = df_copy['Vehicle_Ownership'].map({'Yes': 1, 'No': 0})
    df_copy['Vehicle_Ownership'].fillna(0, inplace=True)

df_copy['EmploymentStatus'] = df_copy['EmploymentStatus'].astype(str).str.lower()
df_copy = pd.get_dummies(df_copy, columns=['EmploymentStatus', 'MaritalStatus'], drop_first=True)
df_copy.drop(['first_name', 'last_name'], axis=1, inplace=True, errors='ignore')

X = df_copy.drop('default', axis=1)
y = df_copy['default']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------------------------------------------------------------------------
# --- Step 7: PCA & SVM Hyperplane Visualization ---
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='coolwarm', edgecolors='k', alpha=0.7)
plt.title('PCA Projection (2D)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Default Status')
plt.show()

svm_mini = SVC(kernel='linear')
svm_mini.fit(X_pca, y)

h = .02
x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z = svm_mini.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.3)
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap=plt.cm.coolwarm, edgecolors='k')
plt.title('SVM Hyperplane Visualization (PCA-reduced Space)')
plt.show()

# -------------------------------------------------------------------------------------------
# --- Step 8: Final Model Training & Formatted Results ---
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Models
svm_model = SVC(kernel='linear', random_state=42).fit(X_train, y_train)
logreg_model = LogisticRegression(random_state=42).fit(X_train, y_train)

# Predictions
y_pred_svm = svm_model.predict(X_test)
y_pred_logreg = logreg_model.predict(X_test)

# --- Visual Confusion Matrices ---
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
sns.heatmap(confusion_matrix(y_test, y_pred_svm), annot=True, fmt='d', cmap='Blues', ax=ax[0])
ax[0].set_title('Confusion Matrix: SVM')
ax[0].set_xlabel('Predicted')
ax[0].set_ylabel('Actual')
sns.heatmap(confusion_matrix(y_test, y_pred_logreg), annot=True, fmt='d', cmap='Greens', ax=ax[1])
ax[1].set_title('Confusion Matrix: Logistic Regression')
ax[1].set_xlabel('Predicted')
ax[1].set_ylabel('Actual')
plt.tight_layout()
plt.show()


# ***** CHANGE IS HERE: FORMATTED TERMINAL OUTPUT *****

# Get classification reports as dictionaries
report_logreg = classification_report(y_test, y_pred_logreg, output_dict=True)
report_svm = classification_report(y_test, y_pred_svm, output_dict=True)

# Extract metrics using weighted average for a balanced view
logreg_metrics = report_logreg['weighted avg']
logreg_accuracy = report_logreg['accuracy']

svm_metrics = report_svm['weighted avg']
svm_accuracy = report_svm['accuracy']

# Print in the requested format
print("\nLogistic Regression Results:")
print(f"Accuracy: {logreg_accuracy:.4f}")
print(f"Precision: {logreg_metrics['precision']:.4f}")
print(f"Recall: {logreg_metrics['recall']:.4f}")
print(f"F1-score: {logreg_metrics['f1-score']:.4f}")

print("\nSVM Results:")
print(f"Accuracy: {svm_accuracy:.4f}")
print(f"Precision: {svm_metrics['precision']:.4f}")
print(f"Recall: {svm_metrics['recall']:.4f}")
print(f"F1-score: {svm_metrics['f1-score']:.4f}")
