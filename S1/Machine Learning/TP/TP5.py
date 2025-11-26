import pandas as pd
import numpy as np

dictionary_1={"Name":["Alex","Mike","John","Dave","Joey"],"Height(m)":[1.75,1.65,1.73,np.nan,1.82],
            "Test Score":[70,np.nan,8,62,73]}
df_1=pd.DataFrame(dictionary_1)

print("df_1:\n",df_1.isnull())
print("\nisnull:\n",df_1.isnull())
df_1=df_1.replace(["-","na"],np.nan)
print("replace non -standard missing values:\n",df_1)
df_1 = df_1.fillna(0)
print("fillna: \n",df_1)

"""""
df=df.fillna('*')
df['Test Score']=df['Test Score'].fillna('*')

df['Test Score']=df['Test Score'].fillna(df['Test Score'].mean())
df['Test Score']=df['Test Score'].fillna(df['Test Score'].interpolate())
df=df.dropna()
df['Height(m)']=df['Height(m)'].dropna()



print("Filling missing values:\n")
print("pad:\n",df.fillna('*').fillna(method='pad'))
"""""

