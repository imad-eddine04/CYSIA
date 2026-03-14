#---------------Phase 1: Pre‑processing (Filtrage & Niveau de Gris)-----------------
#---------------Phase 1: Pre‑processing (Filtrage & Niveau de Gris)-----------------
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image (replace with your own image file)
img_bgr = cv2.imread('CCTV.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)   # for correct display with matplotlib

# Convert to grayscale (Haar cascade needs grayscale)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to smooth out noise (filtre passe‑bas)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Show the results
plt.figure(figsize=(12,4))
plt.subplot(1,3,1); plt.imshow(img_rgb); plt.title('Original Image'); plt.axis('off')
plt.subplot(1,3,2); plt.imshow(gray, cmap='gray'); plt.title('Grayscale'); plt.axis('off')
plt.subplot(1,3,3); plt.imshow(blurred, cmap='gray'); plt.title('After Gaussian Blur'); plt.axis('off')
plt.tight_layout()
plt.show()

#---------------Phase 2: Person Detection with Haar Cascade (Pre‑trained ML)-----------------
#---------------Phase 2: Person Detection with Haar Cascade (Pre‑trained ML)-----------------

# Load the pre‑trained Haar cascade for full body
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Detect people in the blurred grayscale image
# Parameters: scaleFactor, minNeighbors, minSize can be adjusted
boxes = body_cascade.detectMultiScale(blurred, scaleFactor=1.1, minNeighbors=5, minSize=(50, 100))

# Draw bounding boxes on a copy of the original colour image
img_with_boxes = img_rgb.copy()
for (x, y, w, h) in boxes:
    cv2.rectangle(img_with_boxes, (x, y), (x+w, y+h), (255, 0, 0), 2)  # blue boxes

# Show the result
plt.figure(figsize=(8,6))
plt.imshow(img_with_boxes)
plt.title(f'Detected {len(boxes)} person(s)')
plt.axis('off')
plt.show()