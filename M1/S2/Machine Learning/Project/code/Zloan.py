import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------------------------------------------
# --- Step 1: Load the dataset ---
try:
    df = pd.read_csv('Loan.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'Loan.csv' not found. Please ensure the file is in the same directory.")
    exit()

# Display basic info
print("First 5 rows:")
print(df.head())

print("\nData Info:")
print(df.info())
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nUnique values in 'EmploymentStatus' (to check for typos):")
print(df['EmploymentStatus'].unique())

print("\nUnique values in 'MaritalStatus' (to check for typos):")
print(df['MaritalStatus'].unique())

# ----------------------------------------------------------------------------------------------------------------------------
# --- Step 2: Data Cleaning ---

# 1. Create a copy of the dataset
df_copy = df.copy()

# 2. Handle missing values manually
# Note: This dataset appears clean, but we keep this logic for robustness.

# --- Numerical Columns ---
# We include the new numerical columns found in your file
numerical_cols = ['credit_score', 'annual_income', 'loan_amount', 'employment_duration', 'Age', 'Children_Count', 'Previous_Loan_Count']

for col in numerical_cols:
    if col in df_copy.columns:
        mean_val = df_copy[col].mean()
        df_copy[col].fillna(mean_val, inplace=True)

# --- Categorical Columns ---
categorical_cols = ['EmploymentStatus', 'MaritalStatus', 'Vehicle_Ownership']

for col in categorical_cols:
    if col in df_copy.columns:
        mode_val = df_copy[col].mode()[0]
        df_copy[col].fillna(mode_val, inplace=True)

# Verify that there are no more missing values
print("Missing values after manual imputation:")
print(df_copy.isnull().sum())

# ---------------------------------------------------------------------------------------------------

# 3. Handle categorical encoding & Typos
# Fix inconsistencies in 'EmploymentStatus'
# Your file contains 'self-xmployed' and 'unxmployed' which need fixing.
df_copy['EmploymentStatus'] = df_copy['EmploymentStatus'].str.lower().replace({
    'self-emploxed': 'self-employed',
    'self-xmployed': 'self-employed', # New typo found in your file
    'unemploxed': 'unemployed',
    'unxmployed': 'unemployed',       # New typo found in your file
    'xtudent': 'student',
    'exployed': 'employed'
})

# Fix inconsistencies in 'MaritalStatus' (if any)
df_copy['MaritalStatus'] = df_copy['MaritalStatus'].str.lower().replace({
    'divorcxd': 'divorced',
    'marrixd': 'married',
    'maxried': 'married'
})

print("\nUnique values in 'EmploymentStatus' after cleaning:")
print(df_copy['EmploymentStatus'].unique())

# --- Encode Binary Categorical Columns ---

# 'Vehicle_Ownership' is Yes/No. We convert it to 1/0.
if 'Vehicle_Ownership' in df_copy.columns:
    df_copy['Vehicle_Ownership'] = df_copy['Vehicle_Ownership'].map({'Yes': 1, 'No': 0})

# --- One-Hot Encoding for other categorical columns ---
df_copy = pd.get_dummies(df_copy, columns=['EmploymentStatus', 'MaritalStatus'], drop_first=True)

# Drop unrelated columns (Names)
df_copy.drop(['first_name', 'last_name'], axis=1, inplace=True, errors='ignore')

print("\nHead of the dataset after encoding:")
print(df_copy.head())

# --------------------------------------------------------------------------------------------------
# 4. Manage outliers (Simple method using IQR)

# We apply this to continuous numerical features
features_to_check = ['credit_score', 'annual_income', 'loan_amount', 'employment_duration', 'Age']

print("Shape before outlier handling:", df_copy.shape)

for col in features_to_check:
    Q1 = df_copy[col].quantile(0.25)
    Q3 = df_copy[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Cap the outliers
    df_copy[col] = np.where(df_copy[col] < lower_bound, lower_bound, df_copy[col])
    df_copy[col] = np.where(df_copy[col] > upper_bound, upper_bound, df_copy[col])

print("Shape after outlier handling (capping):", df_copy.shape)

# -----------------------------------------------------------------------------------------------
# 5. Feature scaling (StandardScaler)
scaler = StandardScaler()

# We scale all numerical features, including the new counts
# We scale all numerical features, including the new counts
features_to_scale = ['credit_score', 'annual_income', 'loan_amount', 'employment_duration', 'Age', 'Children_Count', 'Previous_Loan_Count']

# Fit the scaler on the data and transform it
df_copy[features_to_scale] = scaler.fit_transform(df_copy[features_to_scale])

print("Head of the dataset after scaling:")
print(df_copy.head())

# --------------------------------------------------------------------------------------

# 6. Train/test split (80/20)

# Separate features (X) and target (y)
X = df_copy.drop('default', axis=1)
y = df_copy['default']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training set size (X_train):", X_train.shape)
print("Testing set size (X_test):", X_test.shape)

# ---------------------------------------------------------------------------------------

# 7. Train SVM (linear kernel)
svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_train, y_train)
print("SVM model training completed.")

# ---------------------------------------------------------------------------------------

# 8. Train Logistic Regression
logreg_model = LogisticRegression(random_state=42)
logreg_model.fit(X_train, y_train)
print("Logistic Regression model training completed.")

# ---------------------------------------------------------------------------------------

# 9. Evaluation & Visualization

# Predict on test set
y_pred_svm = svm_model.predict(X_test)
y_pred_logreg = logreg_model.predict(X_test)

# Confusion Matrices
cm_svm = confusion_matrix(y_test, y_pred_svm)
cm_logreg = confusion_matrix(y_test, y_pred_logreg)

print("Confusion Matrix for SVM:")
print(cm_svm)

print("\nConfusion Matrix for Logistic Regression:")
print(cm_logreg)

# Visualization
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# SVM Plot
ax[0].imshow(cm_svm, cmap='Blues')
ax[0].set_title('SVM Confusion Matrix')
ax[0].set_ylabel('True Label')
ax[0].set_xlabel('Predicted Label')
# Add counts
for i in range(cm_svm.shape[0]):
    for j in range(cm_svm.shape[1]):
        ax[0].text(j, i, cm_svm[i, j], ha='center', va='center', color='black')

# LogReg Plot
ax[1].imshow(cm_logreg, cmap='Greens')
ax[1].set_title('Logistic Regression Confusion Matrix')
ax[1].set_ylabel('True Label')
ax[1].set_xlabel('Predicted Label')
# Add counts
for i in range(cm_logreg.shape[0]):
    for j in range(cm_logreg.shape[1]):
        ax[1].text(j, i, cm_logreg[i, j], ha='center', va='center', color='black')

plt.tight_layout()
plt.show()

# Classification Reports
print("--- SVM Classification Report ---")
print(classification_report(y_test, y_pred_svm))

print("\n--- Logistic Regression Classification Report ---")
print(classification_report(y_test, y_pred_logreg))

# Accuracy Comparison Bar Chart
model_names = ['SVM', 'Logistic Regression']
svm_accuracy = svm_model.score(X_test, y_test)
logreg_accuracy = logreg_model.score(X_test, y_test)
accuracies = [svm_accuracy, logreg_accuracy]

plt.figure(figsize=(8, 6))
plt.bar(model_names, accuracies, color=['blue', 'green'])
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Comparison of Model Accuracy')
plt.ylim(0, 1.0)

for i, v in enumerate(accuracies):
    plt.text(i, v + 0.02, str(round(v, 2)), ha='center', fontweight='bold')

plt.show()

print(f"SVM Accuracy: {svm_accuracy:.2f}")
print(f"Logistic Regression Accuracy: {logreg_accuracy:.2f}")
