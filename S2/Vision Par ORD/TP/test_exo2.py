import cv2
import matplotlib.pyplot as plt

img_d = cv2.imread("img_d.png", cv2.IMREAD_GRAYSCALE)

img_mean = cv2.blur(img_d, (5, 5))

img_median = cv2.medianBlur(img_d, 5)

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(img_d, cmap='gray')
plt.title('Original (Grayscale)')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(img_mean, cmap='gray')
plt.title('Mean Filter 5x5')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(img_median, cmap='gray')
plt.title('Median Filter 5')
plt.axis('off')

plt.tight_layout()
plt.show()
