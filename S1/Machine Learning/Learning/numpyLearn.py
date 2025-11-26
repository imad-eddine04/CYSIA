import numpy as np

a = np.array([1,2,3,4,5])
print(a)

b = np.array([[1, 2, 3],
              [4, 5, 6]])
print(b)


x = np.arange(1, 10, 2)
print(x)   # [1 3 5 7 9]


y = np.linspace(1, 10, 5)
print(y)   # [1. 3.25 5.5 7.75 10.]


z = np.zeros((2, 3))
o = np.ones((3, 3))
print(z)
print(o)


c = np.array([[1, 2, 3],
              [4, 5, 6]])

print(c.dtype)   # data type
print(c.ndim)    # number of dimensions
print(c.shape)   # (rows, columns)
print(c.size)    # total elements
