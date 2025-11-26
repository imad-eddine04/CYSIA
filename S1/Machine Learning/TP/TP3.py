import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


"""""
a = np.array([1, 2, 3])
b = np.array([[1],[2],[3]])
c = np.array([[1, 2, 3], [4, 5, 6]])
print(a)
print(b)
print(c)


d = np.arange(1,10,2)
print("d:",d)


e = np.linspace(1,10,2)
print(e)
f = np.linspace(1,10,5)
print(f)


g = np.zeros(5)
print(g)
h = np.ones((2,5))
print(h)



c.dtype
c.ndim
c.shape
c.size
print(c)

print(c[:,1])
print(c[:,:])
print(c[:,::2])
"""""

"""""
x = np.linspace(0, 2*np.pi, 30)
y = np.cos(x)
print("X:",x)
print("\nY:",y)

plt.figure(figsize=(5,2))
plt.title('ici tp 1')
plt.subplot()
plt.plot(x,y)
plt.xlabel('x')
plt.ylabel('cos(x)')
plt.show()


plt.figure(figsize=(5,4))
plt.title('ici tp 2')
plt.subplot(311)
plt.plot(x,y,'y')
plt.xlabel('x')
plt.ylabel('cos(x)')
plt.subplot(312)
plt.plot(x,np.exp(x))
plt.xlabel('x')
plt.ylabel('exp(x)')
plt.subplot(313)
plt.plot(x,-np.exp(-x))
plt.xlabel('x')
plt.ylabel('-exp(-x)')
plt.show()

"""""
"""""
data = [(1, 2.0, "Hello"), (2, 3.0, "World")]
df = pd.DataFrame(data)
print(df)
df1 = pd.DataFrame(data, index=["premier", "second"], columns=["A", "B", "C"])
print("\n",df1)

d = {"one": [1.0, 2.0, 3.0], "two": [4.0, 3.0, 2.0]}
df = pd.DataFrame(d)
print("\n\n",df)
df1 = pd.DataFrame(d, index=["a", "b", "c"])
print("\n",df1)



data2 = [{"a": 1, "b": 2}, {"a": 5, "b": 10, "c": 20}]
df = pd.DataFrame(data2)
print("\n\n",df)
df1 = pd.DataFrame(data2, index=["first", "second"], columns=["a", "b"])
print("\n",df1)


df.head()

"""""

df2 = pd.DataFrame(np.random.randn(5, 4), index=list('abcde'), columns=list('ABCD'))
print(df2.loc["b"])
print(df2.iloc[1])



print(df2.loc[:, "B"])
print(df2.iloc[:, 1])
print(df2.loc[['a','d'],['B','D']])
print(df2.iloc[[0,3],[1,3]])
print(df2.loc['a':'c','B':'D'])
print(df2.iloc[0:2,1:3])


dff = pd.DataFrame(np.random.randn(7, 3), columns=list("ABC"))
dff.iloc[1:3, 0] = np.nan
dff.iloc[2:4, 1] = np.nan
dff.iloc[3:5, 2] = np.nan



print(dff['A'].isna())
print(dff.notna())

dff['A'].fillna(0.0, inplace= True) 
print(dff)

dff['B'].fillna(dff.mean()['B'], inplace= True)
print(dff)
dff.dropna(axis=0, inplace= True)
print(dff)