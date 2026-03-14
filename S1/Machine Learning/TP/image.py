from sklearn.datasets import fetch_olivetti_faces
import numpy as np
import pandas as pd


data = fetch_olivetti_faces()

images = data.images

features = []

for img in images:
    blocks = []
    h, w = img.shape
    h_step = h // 3
    w_step = w // 3

    for i in range(3):
        for j in range(3):
            block = img[i * h_step:(i + 1) * h_step, j * w_step:(j + 1) * w_step]
            blocks.append(block.mean())

    features.append(blocks)

df = pd.DataFrame(features)

print("Shape du DataFrame :", df.shape)
print(df)
