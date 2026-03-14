from cProfile import label

import pandas as pd
from pyexpat import features

"""""
df = pd.read_csv("plyer.csv", index_col=0)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
print(df)

total     = len(df)
count_yes = (df["Play"] == "Yes").sum()
count_no  = (df["Play"] == "No").sum()
P_yes = count_yes / total
P_no  = count_no  / total

print(f"\nP(Yes) = {count_yes}/{total} = {P_yes:.4f}")
print(f"P(No)  = {count_no}/{total} = {P_no:.4f}")

features = ["Weather", "Temperature"]

def compute_likelihoods(df, features, target="Play"):
    classes = df[target].unique()
    likelihoods = {}
    for feat in features:
        likelihoods[feat] = {}
        for val in df[feat].unique():
            likelihoods[feat][val] = {}
            for cls in classes:
                subset = df[df[target] == cls]
                likelihoods[feat][val][cls] = (subset[feat] == val).sum() / len(subset)
    return likelihoods

likelihoods = compute_likelihoods(df, features)

print("\n Vraisemblances:")
for feat in features:
    rows = []
    for val in likelihoods[feat]:
        n_yes = count_yes
        n_no  = count_no
        p_yes = likelihoods[feat][val]["Yes"]
        p_no  = likelihoods[feat][val]["No"]
        rows.append({
            feat  : val,
            "P(No)" : f"{round(p_no*n_no)}/{n_no} = {p_no:.4f}",
            "P(Yes)": f"{round(p_yes*n_yes)}/{n_yes} = {p_yes:.4f}",
        })
    print(f"\n{feat}:")
    print(pd.DataFrame(rows).set_index(feat).to_string())

def naive_bayes_predict(sample, likelihoods, P_yes, P_no, verbose=True):
    score_yes = P_yes
    score_no  = P_no
    for feat, val in sample.items():
        score_yes *= likelihoods[feat][val]["Yes"]
        score_no  *= likelihoods[feat][val]["No"]
    total_score = score_yes + score_no
    prob_yes = score_yes / total_score
    prob_no  = score_no  / total_score
    if verbose:
        print(f"\nPrediction pour {sample}")
        print(f"P(Yes|today) = {prob_yes:.2f}")
        print(f"P(No|today)  = {prob_no:.2f}")
        print(f"Classe predite : {'Yes' if prob_yes > prob_no else 'No'}")
    return ("Yes" if prob_yes > prob_no else "No"), prob_yes, prob_no

naive_bayes_predict({"Weather": "Overcast", "Temperature": "Mild"}, likelihoods, P_yes, P_no)
"""""


"""
#-----------with the algorithm---------------------
import os
import pandas as pd
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "plyer.csv"), index_col=0)

target   = df.columns[-1]
features = [c for c in df.columns if c != target]
#
# # ── Encode ────────────────────────────────────────────────────────────────────
le_dict = {}
X = df[features].copy()
for col in features:
 le = LabelEncoder()
 X[col] = le.fit_transform(X[col])
 le_dict[col] = le
#
le_y = LabelEncoder()
y = le_y.fit_transform(df[target])
#
# # ── Train ─────────────────────────────────────────────────────────────────────
model = CategoricalNB()
model.fit(X, y)
#
# # ── Test ──────────────────────────────────────────────────────────────────────
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
"""



#import LabelEncoder
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
#converting string lables into numbers
weather_encoded = le.fit_transform(weather)
print("weather: ",weather_encoded)
#converting string lables into numbers
temp_encoded = le.fit_transform(temp)
label = le.fit_transform(play)
print("play: ",label)
print("temp: ",temp_encoded)

features = zip(weather_encoded, temp_encoded)
import numpy as np
features = np.asarray(list(features))
print("features: ", features)

#import Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB
#create a gaussian classifier
model = GaussianNB()
#train the model using the training sets
model.fit(features, label)
#predict output
predicted = model.predict([[0,2]])
print("predicted values (No = 0 , Yes = 1) :  ", predicted)