import numpy as np
import cv2
from matplotlib import pyplot as plt

# Make sure 'smarties.png' is in the same directory as your script
try:
    img = cv2.imread('smarties.png', cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("smarties.png not found. Please download it and place it in the correct directory.")

    # Convert the image to black and white
    # The _ is used to ignore the first return value of the threshold function
    _, img_nb = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY_INV)

    # --- QUESTION SOLVED ---
    # The kernel is replaced with a 3x3 matrix as requested.
    kernel = np.ones((3,3), np.uint8)

    # Perform morphological operations
    dilation = cv2.dilate(img_nb, kernel, iterations=2)
    erosion = cv2.erode(img_nb, kernel, iterations=1)
    opening = cv2.morphologyEx(img_nb, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(img_nb, cv2.MORPH_CLOSE, kernel)

    # Display the results on plots
    titles = ['Original Grayscale', 'Black & White', 'Dilation', 'Erosion', 'Opening', 'Closing']
    images = [img, img_nb, dilation, erosion, opening, closing]

    plt.figure(figsize=(12, 8))
    for i in range(6):
        plt.subplot(2, 3, i + 1)
        plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([]) # Hide axis ticks

    plt.tight_layout()
    plt.show()

except FileNotFoundError as e:
    print(e)
