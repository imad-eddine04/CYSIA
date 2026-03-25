#---------------Phase 1: Pre‑processing (Filtrage & Niveau de Gris)-----------------
#---------------Phase 1: Pre‑processing (Filtrage & Niveau de Gris)-----------------
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image (replace with your own image file)
img_bgr = cv2.imread('Images/HandCamera.png')
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

# Detect people in the grayscale image (less blurring preserves more features)
# Parameters: scaleFactor, minNeighbors, minSize can be adjusted
boxes = body_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(40, 80), flags=cv2.CASCADE_SCALE_IMAGE)

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

#---------------Phase 3: Vest Detection inside Each Bounding Box-----------------
#---------------Phase 3: Vest Detection inside Each Bounding Box-----------------

#---------------Step 3.1: Extract ROI and Binarization (Seuillage)-----------------

def create_vest_mask(roi_bgr):
    """Return a binary mask of pixels that look like a yellow/orange safety vest."""
    # Convert ROI to HSV (easier for colour segmentation)
    hsv = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)

    # Define range for yellow/orange (you may need to tune these)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    # Create binary mask
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    return mask


# Test on the first detected person (if any)
if len(boxes) > 0:
    x, y, w, h = boxes[0]
    roi_bgr = img_bgr[y:y + h, x:x + w]  # crop from original BGR image
    roi_rgb = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2RGB)
    mask = create_vest_mask(roi_bgr)

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1);
    plt.imshow(roi_rgb);
    plt.title('ROI (person)');
    plt.axis('off')
    plt.subplot(1, 3, 2);
    plt.imshow(mask, cmap='gray');
    plt.title('Raw vest mask');
    plt.axis('off')
    plt.show()

# ---------------Step 3.2: Morphological Cleaning (Ouverture & Fermeture)-----------------

# Define a 3x3 structuring element (élément structurant)
kernel = np.ones((3,3), np.uint8)

# Opening: erosion then dilation – removes small noise
mask_opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Closing: dilation then erosion – fills holes in the vest
mask_cleaned = cv2.morphologyEx(mask_opened, cv2.MORPH_CLOSE, kernel)

# Show the results
plt.figure(figsize=(15,4))
plt.subplot(1,4,1); plt.imshow(roi_rgb); plt.title('ROI'); plt.axis('off')
plt.subplot(1,4,2); plt.imshow(mask, cmap='gray'); plt.title('Raw mask'); plt.axis('off')
plt.subplot(1,4,3); plt.imshow(mask_opened, cmap='gray'); plt.title('After opening'); plt.axis('off')
plt.subplot(1,4,4); plt.imshow(mask_cleaned, cmap='gray'); plt.title('After closing'); plt.axis('off')
plt.tight_layout()
plt.show()

#---------------Step 3.3: Decision Rule (Vest Present?)-----------------

# Count white pixels (value 255) in the cleaned mask
vest_pixels = np.sum(mask_cleaned == 255)
roi_area = w * h
vest_ratio = vest_pixels / roi_area

threshold = 0.1   # 10% of ROI area
vest_detected = vest_ratio > threshold

print(f"Vest pixels: {vest_pixels} / {roi_area} = {vest_ratio:.2%}")
print(f"Vest detected: {vest_detected}")

#---------------Phase 4: Final Output – Visualisation with Coloured Boxes-----------------
#---------------Phase 4: Final Output – Visualisation with Coloured Boxes-----------------

# Create a copy of the original colour image for final drawing
final_img = img_rgb.copy()

total_people = len(boxes)
people_with_vest = 0

for (x, y, w, h) in boxes:
    roi_bgr = img_bgr[y:y + h, x:x + w]
    mask = create_vest_mask(roi_bgr)

    # Morphological cleaning
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    vest_pixels = np.sum(mask == 255)
    roi_area = w * h
    vest_ratio = vest_pixels / roi_area

    if vest_ratio > 0.1:  # threshold
        colour = (0, 255, 0)  # green
        people_with_vest += 1
    else:
        colour = (255, 0, 0)  # red (or you can use (255,0,0) for blue, but we'll use red for clarity)
        # Actually let's use red for "no vest": (255,0,0) in RGB is red? Wait: OpenCV uses BGR, but we are using RGB for display.
        # We'll define colours in RGB for matplotlib.
        colour = (255, 0, 0)  # red in RGB

    cv2.rectangle(final_img, (x, y), (x + w, y + h), colour, 3)

# Add text with statistics
text = f'Total people: {total_people} | With vest: {people_with_vest} | Without: {total_people - people_with_vest}'
cv2.putText(final_img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

# Show the final result
plt.figure(figsize=(12, 8))
plt.imshow(final_img)
plt.title('PPE Detection Result')
plt.axis('off')
plt.show()