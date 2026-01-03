#Step 1 — Import libraries + load the dataset
import pandas as pd
import numpy as np


def seperator():
    print("_____________________________________________________________________________________________")

df = pd.read_csv("..\\DataSets\\Salaries.csv")

print(df.head())


seperator()
#Step 2 — Understand the DataFrame (basic checks)
seperator()
print("dataset Shape :",df.shape)
seperator()
print("dataset columns : \n",df.columns.tolist())
seperator()
print("Data Types : \n",df.dtypes)
seperator()
print("Missing Values : \n",df.isna().sum())
seperator()
print("Duplicated rows : ",df.duplicated().sum())
seperator()
print("Target Column : ",df["salary"].name)

seperator()
#Step 3 — Identify the target + classify column types
seperator()

target = "salary"
X = df.drop(columns=[target])
num_cols = X.select_dtypes(include=["number"]).columns.tolist()
cat_cols = X.select_dtypes(exclude=["number"]).columns.tolist()

print("Target:", target)
print("Numeric columns:", num_cols)
print("Categorical columns:", cat_cols)

seperator()
#Step 4 — Create a “practice” dataset with random NaN values
seperator()

print("creating new dataframe (df-dirty) filled randomly with NaN values so we clean it up : \n")

df_dirty = df.copy()

# fixed seed so results are repeatable
rng = np.random.default_rng(12)

# choose how much missingness you want
frac_cat = 0.05   # 5% of rows
frac_num = 0.07   # 7% of rows

# pick random rows for a categorical column (sex)
idx_cat = rng.choice(df_dirty.index, size=int(len(df_dirty) * frac_cat), replace = False)
df_dirty.loc[idx_cat, "sex"] = np.nan

# pick random rows for a numeric column (yrs.service)
idx_num = rng.choice(df_dirty.index, size=int(len(df_dirty) * frac_num), replace=False)
df_dirty.loc[idx_num, "yrs.service"] = np.nan

print(df_dirty.isna().sum())

seperator()
#Step 5 — Handle missing values (NaN) the right way
seperator()

print("using droping method for missing value : \n")
df_drop = df_dirty.dropna()
print("shape before :",df_dirty.shape,"\nshape after :",df_drop.shape)
print(df_drop.isna().sum())

seperator()

print("using filling method for missing value : \n")
df_fill = df_dirty.copy()
seperator()
df_fill["yrs.service"] = df_fill["yrs.service"].fillna(df_fill["yrs.service"].median())
#filling the nan values in sex column with the most frequent values in the column which is male in this case
df_fill["sex"] = df_fill["sex"].fillna(df_fill["sex"].mode()[0])
print("shape before :",df_fill.shape,"\nshape after :",df_fill.shape)
print(df_fill.isna().sum())


seperator()
#Step 6 — Handle the “index” column and prepare X/y
seperator()

unwanted = "Unnamed: 0"
df_fill = df_fill.drop(columns=[unwanted])

print(df_fill.head())

seperator()

x = df_fill.drop(columns=target)
y = df_fill[target]

print("X shape:", X.shape)
print("y shape:", y.shape)
print("\nX head:")
print(X.head())
print("\ny head:")
print(y.head())
seperator()
#Step 7 — Detect salary outliers (and decide what to do with them)
seperator()
print("Salary summary:")
print(df_fill[target].describe())