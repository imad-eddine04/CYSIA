import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# ────────────────────────────────────────────────
# 1. Chargement et prétraitement
# ────────────────────────────────────────────────
file_path = r"password_dataset_500_modified.csv"

df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

numeric_cols = ['Length', 'Has_Upper', 'Has_Lower', 'Has_Digits', 'Has_Special',
                'Unique_Chars', 'Entropy', 'Label']

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['Entropy', 'Label', 'Length', 'Unique_Chars'])

features = ['Length', 'Has_Upper', 'Has_Lower', 'Has_Digits', 'Has_Special',
            'Unique_Chars', 'Entropy']
X = df[features].values
y = df['Label'].values

# Standardisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)



# Séparation train/test (pour les accuracies originales)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.25, random_state=42, stratify=y
)

# ────────────────────────────────────────────────
# 2. Modèles réels (7 features)
# ────────────────────────────────────────────────
models_real = {
    'Linear': SVC(kernel='linear', random_state=42, max_iter=10000),
    'RBF': SVC(kernel='rbf', random_state=42, C=1.0, gamma='scale'),
    'Poly': SVC(kernel='poly', random_state=42, degree=3, C=1.0)
}

predictions_test = {}
accuracies_test = {}

for name, model in models_real.items():
    model.fit(X_train, y_train)
    y_pred_test = model.predict(X_test)
    predictions_test[name] = y_pred_test
    accuracies_test[name] = accuracy_score(y_test, y_pred_test)
    print(f"{name} Test Accuracy (25%): {accuracies_test[name]:.4f}")

# ────────────────────────────────────────────────
# 3. Prédictions et accuracies sur TOUT le dataset (500)
# ────────────────────────────────────────────────
predictions_full = {}
accuracies_full = {}

for name, model in models_real.items():
    y_pred_full = model.predict(X_scaled)  # ← sur tout le dataset
    predictions_full[name] = y_pred_full
    accuracies_full[name] = accuracy_score(y, y_pred_full)
    print(f"{name} Full Dataset Accuracy (500): {accuracies_full[name]:.4f}")

# ────────────────────────────────────────────────
# 4. Visualisation PCA (inchangée)
# ────────────────────────────────────────────────
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

models_pca = {}
for name, params in [
    ('Linear', {'kernel': 'linear', 'random_state': 42, 'max_iter': 10000}),
    ('RBF', {'kernel': 'rbf', 'random_state': 42, 'C': 1.0, 'gamma': 'scale'}),
    ('Poly', {'kernel': 'poly', 'random_state': 42, 'degree': 3, 'C': 1.0})
]:
    clf = SVC(**params)
    clf.fit(X_pca, y)
    models_pca[name] = clf


def plot_decision_boundary(ax, clf, X, y, title):
    h = 0.02
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, alpha=0.25, cmap='RdYlGn')
    ax.contour(xx, yy, Z, colors='black', linewidths=0.8)

    ax.scatter(X[y == 0, 0], X[y == 0, 1], c='green', s=40, edgecolors='black', label='Safe (0)')
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c='red', s=40, edgecolors='black', label='Vulnerable (1)')

    ax.set_title(title)
    ax.set_xlabel('PCA 1')
    ax.set_ylabel('PCA 2')
    ax.legend()
    ax.grid(alpha=0.25)


def visualize_kernels():
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    axes = axes.ravel()

    axes[0].scatter(X_pca[y == 0, 0], X_pca[y == 0, 1], c='green', edgecolors='black', label='Safe')
    axes[0].scatter(X_pca[y == 1, 0], X_pca[y == 1, 1], c='red', edgecolors='black', label='Vulnerable')
    axes[0].set_title("Données originales (PCA 2D)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    for i, (name, clf) in enumerate(models_pca.items(), 1):
        plot_decision_boundary(
            axes[i],
            clf,
            X_pca,
            y,
            f"{name} Kernel (PCA)\nFull acc: {accuracies_full[name]:.4f}"
        )

    plt.tight_layout()
    plt.show()


# ────────────────────────────────────────────────
# 5. Afficher les matrices de confusion sur TOUS les 500
# ────────────────────────────────────────────────
def show_all_confusion_matrices_full():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Confusion Matrices ", fontsize=16, fontweight='bold')

    for idx, (name, y_pred) in enumerate(predictions_full.items()):
        cm = confusion_matrix(y, y_pred)  # ← sur tout le dataset (y, pas y_test)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                    cbar=False, annot_kws={"size": 16})
        axes[idx].set_title(f'{name}\nAccuracy: {accuracies_full[name]:.4f}', fontsize=12)
        axes[idx].set_xlabel('Predicted')
        axes[idx].set_ylabel('Actual')
        axes[idx].set_xticklabels(['Safe', 'Vulnerable'], fontsize=10)
        axes[idx].set_yticklabels(['Safe', 'Vulnerable'], fontsize=10, rotation=0)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# ────────────────────────────────────────────────
# 6. Extraction features + GUI
# ────────────────────────────────────────────────
def extract_features(password):
    if not password:
        return None
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    unique_chars = len(set(password))
    entropy = np.log2(unique_chars) if unique_chars > 0 else 0

    feats = [length, int(has_upper), int(has_lower), int(has_digit),
             int(has_special), unique_chars, entropy]

    return scaler.transform([feats])[0]


root = tk.Tk()
root.title("Password Strength Classifier")
root.geometry("580x580")
root.resizable(False, False)

font_title = ("Segoe UI", 14, "bold")
font_label = ("Segoe UI", 11)
font_btn = ("Segoe UI", 10, "bold")

tk.Label(root, text="Password Strength Predictor", font=font_title, pady=12).pack()

frame_input = tk.Frame(root)
frame_input.pack(pady=10)
tk.Label(frame_input, text="Enter password:", font=font_label).pack(side="left", padx=8)
entry = tk.Entry(frame_input, width=38, font=font_label, show="•")
entry.pack(side="left")

result_label = tk.Label(root, text="", font=("Segoe UI", 12, "bold"), pady=12, fg="#222")
result_label.pack()


def test_password():
    pwd = entry.get().strip()
    if not pwd:
        messagebox.showwarning("Attention", "Veuillez entrer un mot de passe")
        return

    feats = extract_features(pwd)
    if feats is None:
        result_label.config(text="Erreur d'extraction", fg="red")
        return

    pred = models_real['RBF'].predict([feats])[0]

    if pred == 0:
        msg = "SAFE PASSWORD ✅"
        color = "darkgreen"
    else:
        msg = "VULNERABLE PASSWORD ❌"
        color = "darkred"

    result_label.config(text=msg, fg=color)


btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Test Password", command=test_password,
          font=font_btn, bg="#2e7d32", fg="white", width=16).pack(side="left", padx=6)

tk.Button(btn_frame, text="Accuracies (Test Set)",
          command=lambda: messagebox.showinfo("Test Set Accuracies (25%)",
                                              "\n".join([f"• {k:8} : {v:.4f}" for k, v in accuracies_test.items()])),
          font=font_btn, bg="#1565c0", fg="white", width=18).pack(side="left", padx=6)

tk.Button(btn_frame, text="Confusion Matrix ", command=show_all_confusion_matrices_full,
          font=font_btn, bg="#8B4513", fg="white", width=20).pack(side="left", padx=6)

tk.Button(root, text="Visualize Decision Boundaries (PCA)", command=visualize_kernels,
          font=font_btn, bg="#8d5524", fg="white", width=35, height=2).pack(pady=20)

root.mainloop()