import pandas as pd

#loading dataset
df = pd.read_csv('C:\\Users\\T14s\\Desktop\\CYSIA\\S1\\Machine Learning\\TP\\Salaries.csv')

#Fill missing values with a constant

#Fill everything with 0
df_filled = df.fillna(0)

#Fill one column with a constant
#df["Team"] = df["Team"].fillna("Unknown")

#Fill numeric column with mean/median
mean_salary = df["salary"].mean()
df["salary"] = df["salary"].fillna(mean_salary)

median_salary = df["salary"].median()
df["salary"] = df["salary"].fillna(median_salary)



print(df.head(10))
print("mean : ",mean_salary)
print("median : ",median_salary)