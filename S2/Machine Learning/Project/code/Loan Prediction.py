import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
# ────────────────────────────────────────────────
# 1. Chargement et Prétraitement (Based on Zloan.py logic)
# ────────────────────────────────────────────────
file_path = "Loan.csv"

try:
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    print(f"Error: '{file_path}' not found.")
    exit()

# Data Cleaning
df_copy = df.copy()

# Fix inconsistencies (Typos from Zloan.py)
df_copy['EmploymentStatus'] = df_copy['EmploymentStatus'].str.lower().replace({
    'self-emploxed': 'self-employed', 'self-xmployed': 'self-employed',
    'unemploxed': 'unemployed', 'unxmployed': 'unemployed',
    'xtudent': 'student', 'exployed': 'employed'
})
df_copy['MaritalStatus'] = df_copy['MaritalStatus'].str.lower().replace({
    'divorcxd': 'divorced', 'marrixd': 'married', 'maxried': 'married'
})

# Missing Values Imputation
numerical_cols = ['credit_score', 'annual_income', 'loan_amount', 'employment_duration', 'Age', 'Children_Count',
                  'Previous_Loan_Count']
for col in numerical_cols:
    df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
    df_copy[col] = df_copy[col].fillna(df_copy[col].mean())

categorical_cols = ['EmploymentStatus', 'MaritalStatus', 'Vehicle_Ownership']
for col in categorical_cols:
    df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])

# Encoding
if 'Vehicle_Ownership' in df_copy.columns:
    df_copy['Vehicle_Ownership'] = df_copy['Vehicle_Ownership'].map({'Yes': 1, 'No': 0})

# Keep track of categorical columns for GUI consistency later
df_final = pd.get_dummies(df_copy, columns=['EmploymentStatus', 'MaritalStatus'], drop_first=True)
df_final.drop(['first_name', 'last_name'], axis=1, inplace=True, errors='ignore')

# Handle Outliers (Capping)
features_to_check = ['credit_score', 'annual_income', 'loan_amount', 'employment_duration', 'Age']
for col in features_to_check:
    Q1, Q3 = df_final[col].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    df_final[col] = np.clip(df_final[col], Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)

# Features and Target
X = df_final.drop('default', axis=1)
y = df_final['default'].values
feature_names = X.columns.tolist()

# Standardization
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/Test Split (Stratified like Project 1)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.25, random_state=42, stratify=y
)

# ────────────────────────────────────────────────
# 2. Modèles SVM Multi-Kernels (Project 1 Style)
# ────────────────────────────────────────────────
models_real = {
    'Linear': SVC(kernel='linear', random_state=42, max_iter=10000),
    'RBF': SVC(kernel='rbf', random_state=42, C=1.0, gamma='scale'),
    'Poly': SVC(kernel='poly', random_state=42, degree=3, C=1.0)
}

predictions_test = {}
accuracies_test = {}
predictions_full = {}
accuracies_full = {}

for name, model in models_real.items():
    # Training
    model.fit(X_train, y_train)

    # Test Evaluation
    y_pred_test = model.predict(X_test)
    predictions_test[name] = y_pred_test
    accuracies_test[name] = accuracy_score(y_test, y_pred_test)

    # Full Dataset Evaluation (Extra Process)
    y_pred_full = model.predict(X_scaled)
    predictions_full[name] = y_pred_full
    accuracies_full[name] = accuracy_score(y, y_pred_full)

    print(f"{name} -> Test Acc: {accuracies_test[name]:.4f} | Full Acc: {accuracies_full[name]:.4f}")

# ────────────────────────────────────────────────
# 3. Visualisation PCA et Frontières de Décision
# ────────────────────────────────────────────────
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

models_pca = {}
for name, model in models_real.items():
    clf_pca = SVC(kernel=model.kernel, random_state=42)
    clf_pca.fit(X_pca, y)
    models_pca[name] = clf_pca


def plot_decision_boundary(ax, clf, X, y, title):
    h = 0.05
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdYlGn')
    ax.scatter(X[y == 0, 0], X[y == 0, 1], c='green', s=20, label='No Default', edgecolors='k')
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c='red', s=20, label='Default', edgecolors='k')
    ax.set_title(title)
    ax.legend(fontsize='small')


def visualize_analysis():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.ravel()

    # Data Overview
    axes[0].scatter(X_pca[y == 0, 0], X_pca[y == 0, 1], c='green', alpha=0.5, label='No Default')
    axes[0].scatter(X_pca[y == 1, 0], X_pca[y == 1, 1], c='red', alpha=0.5, label='Default')
    axes[0].set_title("Original Data (PCA 2D)")
    axes[0].legend()

    for i, (name, clf) in enumerate(models_pca.items(), 1):
        plot_decision_boundary(axes[i], clf, X_pca, y, f"{name} Kernel Boundary")

    plt.tight_layout()
    plt.show()


# ────────────────────────────────────────────────
# 4. Matrices de Confusion (Seaborn Style)
# ────────────────────────────────────────────────
def show_confusion_matrices():
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for idx, (name, y_pred) in enumerate(predictions_full.items()):
        cm = confusion_matrix(y, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], cbar=False)
        axes[idx].set_title(f'{name} Confusion Matrix\nAcc: {accuracies_full[name]:.4f}')
        axes[idx].set_xticklabels(['No Default', 'Default'])
        axes[idx].set_yticklabels(['No Default', 'Default'])
    plt.show()


# ────────────────────────────────────────────────
# 5. Interface GUI pour Prediction
# ────────────────────────────────────────────────
def predict_loan_status():
    try:
        # Extract inputs from GUI
        data = {
            'credit_score': float(entries['credit_score'].get()),
            'annual_income': float(entries['annual_income'].get()),
            'loan_amount': float(entries['loan_amount'].get()),
            'employment_duration': float(entries['employment_duration'].get()),
            'Age': float(entries['Age'].get()),
            'Children_Count': float(entries['Children_Count'].get()),
            'Previous_Loan_Count': float(entries['Previous_Loan_Count'].get()),
            'Vehicle_Ownership': 1 if vehicle_var.get() == "Yes" else 0
        }

        # One-Hot Encoding for input (matching training feature alignment)
        for emp in ['employed', 'self-employed', 'student', 'unemployed']:
            col = f'EmploymentStatus_{emp}'
            if col in feature_names:
                data[col] = 1 if emp_var.get() == emp else 0

        for mar in ['divorced', 'married', 'single']:
            col = f'MaritalStatus_{mar}'
            if col in feature_names:
                data[col] = 1 if mar_var.get() == mar else 0

        # Organize input in correct order
        input_df = pd.DataFrame([data])[feature_names]
        input_scaled = scaler.transform(input_df)

        # Prediction (Using RBF as preferred model)
        pred = models_real['RBF'].predict(input_scaled)[0]

        result_text = "⚠️ LOAN DEFAULT RISK: HIGH ❌" if pred == 1 else "✅ LOAN STATUS: SAFE (LOW RISK)"
        result_color = "darkred" if pred == 1 else "darkgreen"
        res_label.config(text=result_text, fg=result_color)

    except Exception as e:
        messagebox.showerror("Input Error", f"Please check your inputs.\n{e}")


# GUI Layout
root = tk.Tk()
root.title("Loan Default Risk Predictor")
root.geometry("500x700")

tk.Label(root, text="Loan Risk Analysis", font=("Arial", 16, "bold"), pady=10).pack()

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

entries = {}
fields = ['credit_score', 'annual_income', 'loan_amount', 'employment_duration', 'Age', 'Children_Count',
          'Previous_Loan_Count']
for field in fields:
    row = tk.Frame(form_frame)
    row.pack(fill="x", pady=2)
    tk.Label(row, text=field.replace('_', ' ').title(), width=20, anchor="w").pack(side="left")
    ent = tk.Entry(row)
    ent.pack(side="right", expand=True, fill="x")
    entries[field] = ent

# Categorical Dropdowns
tk.Label(form_frame, text="Employment Status").pack(anchor="w")
emp_var = tk.StringVar(value="employed")
ttk.Combobox(form_frame, textvariable=emp_var, values=['employed', 'self-employed', 'student', 'unemployed']).pack(
    fill="x")

tk.Label(form_frame, text="Marital Status").pack(anchor="w")
mar_var = tk.StringVar(value="single")
ttk.Combobox(form_frame, textvariable=mar_var, values=['divorced', 'married', 'single']).pack(fill="x")

tk.Label(form_frame, text="Vehicle Ownership").pack(anchor="w")
vehicle_var = tk.StringVar(value="No")
ttk.Combobox(form_frame, textvariable=vehicle_var, values=['No', 'Yes']).pack(fill="x")

res_label = tk.Label(root, text="", font=("Arial", 12, "bold"), pady=20)
res_label.pack()

tk.Button(root, text="Predict Default Risk", command=predict_loan_status, bg="#1565c0", fg="white",
          font=("Arial", 10, "bold"), height=2).pack(fill="x", padx=50)
tk.Button(root, text="Show Accuracy Metrics", command=lambda: messagebox.showinfo("Metrics",
                                                                                  f"Test Accuracies:\nLinear: {accuracies_test['Linear']:.4f}\nRBF: {accuracies_test['RBF']:.4f}\nPoly: {accuracies_test['Poly']:.4f}"),
          bg="#2e7d32", fg="white").pack(fill="x", padx=50, pady=5)
tk.Button(root, text="Visualize Boundaries & Matrices",
          command=lambda: [visualize_analysis(), show_confusion_matrices()], bg="#8d5524", fg="white").pack(fill="x",
                                                                                                            padx=50)

root.mainloop()

# Save both model and scaler to the requested filename
pickle.dump({'model': model, 'scaler': scaler, 'columns': X.columns.tolist()}, open('Application web/bedad_Loan.sav', 'wb'))
print("Model saved as bedad_Loan.sav")
