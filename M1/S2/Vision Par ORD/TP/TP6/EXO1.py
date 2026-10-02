import numpy as np
import matplotlib.pyplot as plt
import cv2

# --- Dilation ---

# Original image for dilation, converted to uint8 for opencv
image_test_dilation = np.array([
    [0,0,0,0,0],
    [0,1,0,0,0],
    [0,0,0,0,0],
    [0,0,0,1,0],
    [0,0,0,0,0],
    [0,1,0,0,0]
], dtype=np.uint8) * 255 # Use 255 for white pixels

# Structuring element equivalent to skimage's disk(2)
# The diameter is 2*radius + 1
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Dilation with the kernel
dilated_image = cv2.dilate(image_test_dilation, kernel, iterations=1)

# --- Erosion ---

# Original image for erosion, converted to uint8 for opencv
image_test_erosion = np.array([
    [0,0,0,0,0],
    [0,0,1,0,0],
    [0,1,1,1,0],
    [0,0,1,0,0],
    [0,0,0,0,0]
], dtype=np.uint8) * 255 # Use 255 for white pixels

# Erosion with the same kernel
eroded_image = cv2.erode(image_test_erosion, kernel, iterations=1)

# --- Visualization ---

fig, axes = plt.subplots(2, 2, figsize=(8, 8))

# Dilation plots
axes[0, 0].imshow(image_test_dilation, cmap='gray')
axes[0, 0].set_title('Original Image for Dilation')
axes[0, 1].imshow(dilated_image, cmap='gray')
axes[0, 1].set_title('Image after Dilation with disk(2)')

# Erosion plots
axes[1, 0].imshow(image_test_erosion, cmap='gray')
axes[1, 0].set_title('Original Image for Erosion')
axes[1, 1].imshow(eroded_image, cmap='gray')
axes[1, 1].set_title('Image after Erosion with disk(2)')

for ax in axes.ravel():
    ax.axis('off')

plt.tight_layout()
plt.show()

# Print arrays, converting back to 0s and 1s for clarity
print("--- Dilation Result (disk(2)) ---")
print(dilated_image.astype(int) // 255)

print("\n--- Erosion Result (disk(2)) ---")
print(eroded_image.astype(int) // 255)
