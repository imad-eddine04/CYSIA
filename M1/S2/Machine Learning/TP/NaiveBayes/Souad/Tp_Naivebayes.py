import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "plyer.csv"), index_col=0)

target   = df.columns[-1]
features = [c for c in df.columns if c != target]

yes   = len(df[df[target] == 'Yes'])
no    = len(df[df[target] == 'No'])
total = len(df)

# ── Frequency tables ──────────────────────────────────────────────────────────
for feature in features:
    print(f"\n=== {feature} ===")
    rows = []
    for val in df[feature].unique():
        n_yes = len(df[(df[feature] == val) & (df[target] == 'Yes')])
        n_no  = len(df[(df[feature] == val) & (df[target] == 'No')])
        rows.append({feature: val, 'No': n_no, 'Yes': n_yes,
                     'P(val|No)':  f"{n_no}/{no}",
                     'P(val|Yes)': f"{n_yes}/{yes}"})
    rows.append({feature: 'Total', 'No': no, 'Yes': yes,
                 'P(val|No)':  f"{no}/{total}",
                 'P(val|Yes)': f"{yes}/{total}"})
    print(pd.DataFrame(rows).set_index(feature).to_string())

# ── Naive Bayes prediction ────────────────────────────────────────────────────
def predict(sample: dict):
    """
    P(Yes|X) = P(f1|Yes) * P(f2|Yes) * ... * P(Yes)
    P(No |X) = P(f1|No)  * P(f2|No)  * ... * P(No)
    """
    p_yes = yes / total
    p_no  = no  / total

    print("\n── Calcul Naive Bayes ──")
    print(f"P(Yes) = {yes}/{total}    P(No) = {no}/{total}")

    for feat, val in sample.items():
        n_yes_f = len(df[(df[feat] == val) & (df[target] == 'Yes')])
        n_no_f  = len(df[(df[feat] == val) & (df[target] == 'No')])
        print(f"P({feat}={val}|Yes) = {n_yes_f}/{yes}    P({feat}={val}|No) = {n_no_f}/{no}")
        p_yes *= n_yes_f / yes
        p_no  *= n_no_f  / no

    print(f"\nP(Yes|X) = {p_yes:.6f}")
    print(f"P(No |X) = {p_no:.6f}")
    pred = 'Yes' if p_yes > p_no else 'No'
    print(f"→ Prediction : {pred}")
    return pred

# ── Test ──────────────────────────────────────────────────────────────────────
print("\nColumns :", features, "→ Target :", target)

sample = {"Weather": "Overcast", "Temperature": "Mild"}
predict(sample)




#-----------with the algorithm---------------------
import os
import pandas as pd
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "plyer.csv"), index_col=0)

target   = df.columns[-1]
features = [c for c in df.columns if c != target]

# ── Encode ────────────────────────────────────────────────────────────────────
le_dict = {}
X = df[features].copy()
for col in features:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    le_dict[col] = le

le_y = LabelEncoder()
y = le_y.fit_transform(df[target])

# ── Train ─────────────────────────────────────────────────────────────────────
model = CategoricalNB()
model.fit(X, y)

# ── Test ──────────────────────────────────────────────────────────────────────
sample = {}
for f in features:
    val = input(f"Enter {f}: ")
    sample[f] = val

x_sample = pd.DataFrame([{f: le_dict[f].transform([v])[0] for f, v in sample.items()}])
proba = model.predict_proba(x_sample)[0]
pred  = le_y.inverse_transform(model.predict(x_sample))[0]

print("Sample :", sample)
for cls, p in zip(le_y.classes_, proba):
    print(f"P({cls}|X) = {p:.6f}")
print(f"→ Prediction : {pred}")





#--------Gaussian Naive Bayes Classification--------------
import os
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "plyer.csv"), index_col=0)

target   = df.columns[-1]
features = [c for c in df.columns if c != target]

# ── Encode ────────────────────────────────────────────────────────────────────
le_dict = {}
X = df[features].copy()
for col in features:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    le_dict[col] = le

le_y = LabelEncoder()
y = le_y.fit_transform(df[target])

# ── Train ─────────────────────────────────────────────────────────────────────
model = GaussianNB()
model.fit(X, y)

# ── Test ──────────────────────────────────────────────────────────────────────
sample = {}
for f in features:
    val = input(f"Enter {f} {list(df[f].unique())}: ")
    sample[f] = val.strip().capitalize()

x_sample = pd.DataFrame([{f: le_dict[f].transform([v])[0] for f, v in sample.items()}])
proba = model.predict_proba(x_sample)[0]
pred  = le_y.classes_[proba.argmax()]

print("\nSample :", sample)
for cls, p in zip(le_y.classes_, proba):
    print(f"P({cls}|X) = {p:.6f}")
print(f"→ Prediction : {pred}")










