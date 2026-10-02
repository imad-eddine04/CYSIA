from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

from sklearn.datasets import fetch_california_housing

dat = fetch_california_housing()
X = dat.data
y = dat.target

model = LinearRegression()

def plot_learning_curves(model, X, y):
    from sklearn.metrics import mean_squared_error
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    train_errors, val_errors = [], []
    for m in range(1, len(X_train)):
        model.fit(X_train[:m], y_train[:m])
        y_train_predict = model.predict(X_train[:m])
        y_val_predict = model.predict(X_val)
        train_errors.append(mean_squared_error(y_train_predict, y_train[:m]))
        val_errors.append(mean_squared_error(y_val_predict, y_val))
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(np.sqrt(train_errors), "r-+", linewidth=2, label="train")
    ax.plot(np.sqrt(val_errors), "b-", linewidth=3, label="val")
    ax.legend(loc='upper right', bbox_to_anchor=(0.5, 1.1),ncol=1, fancybox=True, shadow=True)
    ax.set_xlabel('Training set size')
    ax.set_ylabel('RMSE')
    plt.show()

plot_learning_curves(model, X, y)


