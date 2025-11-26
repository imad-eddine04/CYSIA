import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.pyplot import xlabel
from unicodedata import numeric

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
#     'Name': ['Adnane', 'Mohamed', 'John', 'Dave', 'Joey'],
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
"""""
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
#plt.show()
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
plt.show()

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


duplicate_rows = df[df.duplicated()]
print("number of duplicate rows (before) :", duplicate_rows.shape)
df.drop_duplicates(inplace=True)
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

sns.displot(df["yrs.service"])
plt.show()

df.groupby(["rank"])["salary"].count().plot(kind="bar")
plt.show()

sns.set_style("whitegrid")
sns.barplot(x="rank", y="salary", data=df, estimator=len)
plt.show()

sns.barplot(x="rank", y="salary", hue="sex", data=df, estimator=len)
plt.show()

sns.barplot(x="discipline", y="salary", hue="rank", data=df, estimator=len)
sns.catplot(x="rank", hue="sex", col="discipline",data=df, kind="count",height=4, aspect=.9)
#plt.show()

df_not_num = df.select_dtypes(include = ["O"])
print("There is : ", len(df_not_num.columns), " non numerical features including : \n",df_not_num.columns.tolist())

print("-----------------------------------------------------")

fig, axes = plt.subplots(round(len(df_not_num.columns) / 3), 3, figsize=(8, 5))
for i, ax in enumerate(fig.axes):
    if i < len(df_not_num.columns):
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)
        sns.countplot(x=df_not_num.columns[i], alpha=0.7, data=df_not_num, ax=ax)
fig.tight_layout()
plt.show()

sns.scatterplot(data=df, x="yrs.since.phd", y="salary")
plt.show()


sns.regplot(x="yrs.since.phd", y="salary", data=df)
plt.show()

sns.pairplot(df)
plt.show()

"""""

Q1 = df.quantile(0.25, numeric_only=True)
Q3 = df.quantile(0.75, numeric_only=True)

IQR = Q3 - Q1
print("Q1 \n",Q1)
print("Q3 \n",Q3)
print("IQR \n",IQR)
print("\n")
df.boxplot()
plt.show()

sns.boxplot(x="rank", y="salary", data=df)
plt.show()
sns.swarmplot(x="rank", y="salary", data=df,color=".25")
plt.show()
sns.boxplot(x="rank", y="salary", data=df,hue="sex")
plt.show()


def remove_outlier(col):
    sorted(col)
    Q1, Q3 = col.quantile([0.25, 0.75])
    IQR = Q3 - Q1
    print("Q1 =", Q1, ", Q3 =", Q3, ", IQR =", IQR)
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)
    return lower_range, upper_range

df_copy = df.copy()
print("shape (before): ", df_copy.shape)

lower_range, upper_range = remove_outlier(df_copy["salary"])
df_copy["salary"] = np.where(df_copy["salary"] < lower_range, lower_range, df_copy["salary"])
df_copy["salary"] = np.where(df_copy["salary"] > upper_range, upper_range, df_copy["salary"])

print("shape (after): ", df_copy.shape)
print("\n")
df_copy.boxplot(column=["salary"])
plt.show()
df_copy = df.copy()

median = df_copy["salary"].quantile(0.50)
print("median =", median)

max_outlier_val = df_copy["salary"].quantile(0.95)

df_copy["salary"] = np.where(df_copy["salary"] > max_outlier_val, median, df_copy["salary"])

print("\n")

df_copy.boxplot(column=["salary"])
plt.show()