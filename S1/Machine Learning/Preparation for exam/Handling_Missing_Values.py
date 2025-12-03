import pandas as pd

#loading dataset
df = pd.read_csv('C:\\Users\\T14s\\Desktop\\CYSIA\\S1\\Machine Learning\\TP\\employees.csv')


df["Team"] = df["Team"].fillna("Zahiyaaaaaaaaaaaaa")
#check how many missing values per column
print(df.isnull())

df_drop = df.dropna()
print(df_drop)

df["Team"] = df["Team"].fillna("Unknown")

mean_salary = df["Salary"].mean()
df["Salary"] = df["Salary"].fillna(mean_salary)


print(df)

print(mean_salary)

""""
#Remove rows with missing values
df_clean = df.dropna()

#Drop rows only if all values are missing
df_clean = df.dropna(how="all")

#Drop columns with too many missing values
df_clean = df.dropna(axis=1)

"""
