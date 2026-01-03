import pandas as pd
#read data set
df = pd.read_csv('..\\DataSets\\Salaries.csv')

#show first 5 rows
print(df.head())

#show the size of the dataset
print(df.shape)

#show informations about dataset
print(df.info())

#compute statistics for numeric columns
print(df.describe())