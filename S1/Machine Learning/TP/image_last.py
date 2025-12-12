import cv2
import mahotas
import numpy as np
from sklearn.datasets import fetch_olivetti_faces
import matplotlib.pyplot as plt

data = fetch_olivetti_faces()
plt.imshow(data.images[0])

hu_mot = hu_moments(data.images[0])
print('hu_mot =', len(hu_mot), '\n', 'hu_mot')

hist = histogram(data.images[0])
print('hist =', len(hist), '\n', 'hist')

haralick = haralick_moments(data.images[0])
print('haralick =', len(haralick), '\n', 'haralick')

desc = ZernikeMoments(21)
zernike = desc.describe(data.images[0])
print('zernike =', len(zernike), '\n', 'zernike')
