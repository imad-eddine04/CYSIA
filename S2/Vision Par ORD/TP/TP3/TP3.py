import cv2
import matplotlib.pyplot as plti
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('test1.jpg')
# informations
print( 'classe :', type(image) )
print( 'type :', image.dtype   )
print( 'taille :', image.shape )

plt.imshow(image)
plt.show()

b, g, r = cv2.split(image)
cv2.imshow('img1',b)
cv2.imshow('img2',g)
cv2.imshow('img3',r)
image = cv2.merge([r, g, b])
plt.imshow(image)
plt.show()

cv2.imwrite('visages.png', image)

hist_image = cv2.calcHist([image],[1],None,[256],[0,256])
plt.plot(hist_image)
plt.xlim([0,256]) #facultatif
plt.show()

plt.plot(hist_image,color='r')