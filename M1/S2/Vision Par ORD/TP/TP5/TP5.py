import cv2
import random
import numpy as np
from skimage.filters import gaussian, median
from skimage.morphology import disk
import matplotlib.pyplot as plt
import os


# --- Helper Functions ---

def create_dummy_images():
    """Creates dummy images if the original files are not found."""
    # Create a placeholder for 'match.jfif'
    if not os.path.exists('match.jfif'):
        print("Creating dummy 'match.jfif'")
        dummy_img_match = np.ones((512, 512), dtype=np.uint8) * 128
        cv2.putText(dummy_img_match, 'match.jfif placeholder', (50, 256), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (255, 255, 255), 2)
        cv2.imwrite('match.jfif', dummy_img_match)

    # Create a placeholder for 'Img_br.jpg'
    if not os.path.exists('Img_br.jpg'):
        print("Creating dummy 'Img_br.jpg'")
        dummy_img_br = np.zeros((512, 512), dtype=np.uint8)
        cv2.rectangle(dummy_img_br, (100, 100), (412, 412), (255, 255, 255), -1)
        cv2.putText(dummy_img_br, 'Img_br.jpg placeholder', (50, 256), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
        cv2.imwrite('Img_br.jpg', dummy_img_br)


def add_noise(img):
    """Adds salt and pepper noise to a grayscale image."""
    img_noise = img.copy()
    row, col = img_noise.shape

    # Add salt (white pixels)
    for _ in range(random.randint(300, 10000)):
        y_coord, x_coord = random.randint(0, row - 1), random.randint(0, col - 1)
        img_noise[y_coord][x_coord] = 255

    # Add pepper (black pixels)
    for _ in range(random.randint(300, 10000)):
        y_coord, x_coord = random.randint(0, row - 1), random.randint(0, col - 1)
        img_noise[y_coord][x_coord] = 0
    return img_noise


# --- Main Execution ---

# 1. Create dummy images if needed
create_dummy_images()

# 2. Process the first image ('match.jfif')
try:
    # Load original image
    img_original = cv2.imread('match.jfif', cv2.IMREAD_GRAYSCALE)
    if img_original is None:
        raise FileNotFoundError("'match.jfif' not found.")

    # Add noise and save
    img_noisy = add_noise(img_original.copy())
    cv2.imwrite('match_bruit.jpg', img_noisy)

    # Apply filters to the noisy image
    gauss_filtered = cv2.GaussianBlur(img_noisy, (5, 5), 0)
    median_filtered = cv2.medianBlur(img_noisy, 5)
    mean_filtered = cv2.blur(img_noisy, (5, 5))

    # --- Plotting results for the first image ---
    plt.figure(figsize=(12, 10))
    plt.suptitle("Filtering results for 'match.jfif'", fontsize=16)

    plt.subplot(2, 3, 1)
    plt.imshow(img_original, cmap='gray')
    plt.title('Original')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.imshow(img_noisy, cmap='gray')
    plt.title('Salt & Pepper Noise')
    plt.axis('off')

    # Empty subplot for layout
    plt.subplot(2, 3, 3)
    plt.axis('off')

    plt.subplot(2, 3, 4)
    plt.imshow(gauss_filtered, cmap='gray')
    plt.title('Gaussian Filter')
    plt.axis('off')

    plt.subplot(2, 3, 5)
    plt.imshow(median_filtered, cmap='gray')
    plt.title('Median Filter')
    plt.axis('off')

    plt.subplot(2, 3, 6)
    plt.imshow(mean_filtered, cmap='gray')
    plt.title('Mean Filter')
    plt.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


except FileNotFoundError as e:
    print(e)

# 3. Process the second image ('Img_br.jpg')
try:
    img_br_original = cv2.imread('Img_br.jpg', cv2.IMREAD_GRAYSCALE)
    if img_br_original is None:
        raise FileNotFoundError("'Img_br.jpg' not found.")

    # Apply filters to the original 'Img_br.jpg'
    img_br_gauss = cv2.GaussianBlur(img_br_original, (5, 5), 0)
    img_br_median = cv2.medianBlur(img_br_original, 5)
    img_br_mean = cv2.blur(img_br_original, (5, 5))

    # --- Plotting results for the second image ---
    plt.figure(figsize=(15, 5))
    plt.suptitle("Filtering results for 'Img_br.jpg'", fontsize=16)

    plt.subplot(1, 4, 1)
    plt.imshow(img_br_original, cmap='gray')
    plt.title('Original')
    plt.axis('off')

    plt.subplot(1, 4, 2)
    plt.imshow(img_br_gauss, cmap='gray')
    plt.title('Gaussian Filter')
    plt.axis('off')

    plt.subplot(1, 4, 3)
    plt.imshow(img_br_median, cmap='gray')
    plt.title('Median Filter')
    plt.axis('off')

    plt.subplot(1, 4, 4)
    plt.imshow(img_br_mean, cmap='gray')
    plt.title('Mean Filter')
    plt.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


except FileNotFoundError as e:
    print(e)

# Show all the plots
plt.show()
