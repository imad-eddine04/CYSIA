import cv2
import numpy as np
from matplotlib import pyplot as plt
img1 = cv2.imread("Image 2 Back.png");
img2 = cv2.imread("Image 2.png");

img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
#enregistrer les informations de img1
height, width , color_scale = img1.shape
dim = (width, height)
# modifier les informations de img2
img2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)
print( 'Original Dimensions img1 : ', img1. shape)
print( 'Original Dimensions img2 : ', img2. shape)
add_img = cv2.add(img1, img2);
plt.imshow(add_img)
plt.show()

Sub_img=cv2.subtract(img1, img2)

mult_img = cv2.multiply(img1, img2)
mult_img = cv2.multiply(img1, 1.5)

plt.subplot(1,3,1),plt.imshow(img1)
plt.title('image 1')
plt.xticks([]),plt.yticks([])
plt.subplot(1,3,2),plt.imshow(img2)
plt.title('image 2')
plt.xticks([]),plt.yticks([])
plt.subplot(1,3,3),plt.imshow(add_img)
plt.title('sub')
plt.xticks([]),plt.yticks([])
plt.show()