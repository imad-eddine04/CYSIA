import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.impute import SimpleImputer
from matplotlib import pyplot as plt


df = pd.read_csv('Salaries.csv', index_col=0)
print(df.shape)
print(df.info())
print("----------------------------------------------------------------------")
print(df.head(10))
print("----------------------------------------------------------------------")
print("----------------------------------------------------------------------")
print(df.tail(10))
print("----------------------------------------------------------------------")
print(df.dtypes)
print(df.describe())
print("----------------------------------------------------------------------")
print("\n")
print("yrs.since.phd:")
print(df["yrs.since.phd"].describe())
"""""
print("----------------------------------------------------------------------")
df["yrs.since.phd"].hist(figsize=(8, 10), bins=100, legend=True, xlabelsize=8, ylabelsize=10)
plt.show()
"""""

print("All types :",list(set(df.dtypes.tolist())))
print("----------------------------------------------------------------------")
df_num = df.select_dtypes(include=["int64"])
print(df_num.head(5))
df_num.hist(figsize=(12, 16), bins=50, xlabelsize=8, ylabelsize=8)
plt.show()