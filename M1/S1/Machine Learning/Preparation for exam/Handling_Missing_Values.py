import pandas as pd

#loading dataset
df = pd.read_csv('..\\DataSets\\employees.csv')


df["Team"] = df["Team"].fillna("Uknowen")
#check how many missing values per column
print(df.isnull())

df_drop = df.dropna()
print(df_drop)



mean_salary = df["Salary"].mean()
df["Salary"] = df["Salary"].fillna(mean_salary)


print(df.to_string())

print(mean_salary)

""""
#Remove rows with missing values
df_clean = df.dropna()

#Drop rows only if all values are missing
df_clean = df.dropna(how="all")

#Drop columns with too many missing values
df_clean = df.dropna(axis=1)

"""
