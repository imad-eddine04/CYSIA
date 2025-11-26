import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.pyplot import xlabel

# dictionary = {
#     'Name': ['Amine', 'Mohamed', 'John', 'Dave', 'Joey'],
#     'Height(m)': [1.86, 1.80, 1.50, np.nan, 1.78],
#     'Test Score': [70, np.nan, 8, 62, 73]
# }
# df = pd.DataFrame(dictionary)
# print(df, end='\n\n\n')
# print(df.shape, end='\n\n\n')
# # df.fillna(0, inplace=True)
# print(df, end='\n\n\n')
#
# print(df.dtypes)
# print(df.head(2), end='\n\n\n')
# print(df.tail(2), end='\n\n\n')
# print(df.isnull())
# print('SUM: \n', df.isnull().sum())

# df['Test Score'] = df['Test Score'].fillna('*')
# print(df, end='\n\n\n')
# df['Test Score'] = df['Test Score'].fillna(df['Test Score'].mean())
# print(df, end='\n\n\n')
# df['Test Score'] = df['Test Score'].fillna(df['Test Score'].interpolate())
# print(df, end='\n\n\n')
# print(df.dropna())
# print('Pad: \n\n\n', df.fillna(method='pad'))

# dictionary_1 = {
#     'Name': ['Amine', 'Mohamed', 'John', 'Dave', 'Joey'],
#     'Height(m)': [1.86, 1.80, '-', 'na', 1.78],
#     'Test Score': [70, np.nan, 8, 62, 73]
# }
# df_1 = pd.DataFrame(dictionary_1)
# print(df_1, end='\n\n\n')
# print(df_1.shape, end='\n\n\n')
# print('isnul: \n\n\n', df_1.isnull())
# df_1 = df_1.replace(['-', 'na'], np.nan)
# print(df_1, end='\n\n\n')

# data = pd.read_csv('C:\DataSets\Dataset\employees.csv')
# # print(data, end='-----------------------------------------------------\n')
# print(data.shape, end='\n-----------------------------------------------------\n')
# print(data.head(2), end='\n-----------------------------------------------------\n')
# print(data.tail(2), end='\n-----------------------------------------------------\n')
# sns.heatmap(data.isnull(), cbar=False, yticklabels=False, cmap='viridis')
# plt.show()

df = pd.read_csv("Salaries.csv", index_col=0)
# df = pd.read_csv("C:\DataSets\Dataset\Salaries.csv")
print(df.shape, end='\n-----------------------------------------------------\n')
print(df.info(), end='\n-----------------------------------------------------\n')
print(df.head(2), end='\n-----------------------------------------------------\n')
print(df.tail(2), end='\n---------------------------------------------------\n')
print(df.dtypes, end='\n-----------------------------------------------------\n')
print(df.describe(), end='\n---------------------------------------------------\n')
print(df['yrs.since.phd'].describe(), end='\n----------------------------------------------------\n')
df = df.replace(['-', 'na'], np.nan)
df['yrs.since.phd'].hist(
    figsize=(8, 10),
    bins=100,
    legend=True,
    xlabelsize=8,
    ylabelsize=8
)

# plt.show()
# print(
#     'All types: ',
#     list(set(df.dtypes.tolist())),
#     end='\n---------------------------------------------------\n'
# )
# df_num = df.select_dtypes(include=['int64'])
# print(
#     df_num.head(5),
#     end='\n-----------------------------------------------------\n'
# )
# df_num.hits(
#     figsize = (12, 16),
#     bins = 50,
#     xlabelsize=8,
#     ylabelsize=8
# )
# plt.show()
print(df.corr(numeric_only=True), end='\n-------------------------------------------------------\n')
corrMatrix = df.corr(numeric_only=True)
sns.heatmap(
    corrMatrix,
    annot=True,
    linewidths=0.01,
    square=True,
    cmap='RdBu',
    linecolor='black',
)
"""""
print("sex : \n", df["sex"].value_counts())
print("\n")
print("discipline : \n", df["discipline"].value_counts())
print("\n")

print("--------------------------------------------------")
print(df["sex"].value_counts(normalize=True))
print("\n")
print(df["discipline"].value_counts(normalize=True))
print("\n")

print("--------------------------------------------------")
df["sex"].value_counts().plot.bar(title="Sex")

df_copy = df.copy()

df_copy = df_copy.drop(["rank", "sex"], axis=1)
print(df_copy.head(5))
"""""

duplicate_rows = df[df.duplicated()]
print("number of duplicate rows (before) :", duplicate_rows.shape)

df.drop_duplicates(inplace=True)

duplicate_rows = df[df.duplicated()]
print("number of duplicate rows (after) :", duplicate_rows.shape)
print("shape :", df.shape)

df_sorted = df.sort_values(by="salary", ascending=False)
print(df_sorted.head(10))


df_copy = df.copy()
print(df.head(10))
print("--------------------------------------------------")
df_copy["sex"] = df_copy["sex"].map({"Male":0, "Female":1})
print("sex : \n", df_copy["sex"].head(10))
print("--------------------------------------------------")
print("rank : \n", df["rank"].value_counts())
print("\n")

df_copy["rank"] = df_copy["rank"].map({"Prof":0, "AsstProf":1, "AssocProf":2})
print("rank : \n", df_copy["rank"].head(10))

sns.distplot(df["yrs.service"])
plt.show()