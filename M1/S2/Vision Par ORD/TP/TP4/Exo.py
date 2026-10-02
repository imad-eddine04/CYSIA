import cv2
import numpy as np
import matplotlib.pyplot as plt



img1_simple = np.zeros((200, 200, 3), dtype=np.uint8)
img1_simple[50:150, 50:150] = (0, 255, 0) # Vert


img2_simple = np.zeros((200, 200, 3), dtype=np.uint8)
cv2.circle(img2_simple, (125, 100), 50, (255, 0, 0), -1) # Rouge


add_img = cv2.add(img1_simple, img2_simple)
mult_img = cv2.multiply(img1_simple, img2_simple)
sub_img = cv2.subtract(img1_simple, img2_simple)




# Charger les images 'Internet' (fournies dans le TP)
img_internet1 = cv2.imread("Image 2 Back.png")
img_internet2 = cv2.imread("Image 2.png")

# Convertir de BGR (OpenCV) à RGB (Matplotlib) pour un affichage correct
img_internet1 = cv2.cvtColor(img_internet1, cv2.COLOR_BGR2RGB)
img_internet2 = cv2.cvtColor(img_internet2, cv2.COLOR_BGR2RGB)

# Redimensionner la deuxième image pour qu'elle ait la même taille que la première
height, width, _ = img_internet1.shape
dim = (width, height)
img_internet2_resized = cv2.resize(img_internet2, dim, interpolation=cv2.INTER_AREA)

# Soustraire les images pour ne garder que les différences
sub_internet = cv2.subtract(img_internet1, img_internet2_resized)


# --- Exercice 2: Afficher les images et les résultats sur le même plot ---

# Créer une figure pour afficher tous les résultats
plt.figure(figsize=(12, 10))
plt.suptitle("Résultats des Opérations sur Images - TP4", fontsize=16)

# Affichage des images simples et des opérations
plt.subplot(2, 4, 1)
plt.imshow(img1_simple)
plt.title("Image Simple 1")
plt.axis('off')

plt.subplot(2, 4, 2)
plt.imshow(img2_simple)
plt.title("Image Simple 2")
plt.axis('off')

plt.subplot(2, 4, 5)
plt.imshow(add_img)
plt.title("Addition")
plt.axis('off')

plt.subplot(2, 4, 6)
plt.imshow(mult_img)
plt.title("Multiplication")
plt.axis('off')

plt.subplot(2, 4, 7)
plt.imshow(sub_img)
plt.title("Soustraction")
plt.axis('off')

# Affichage des images 'Internet' et de la soustraction
plt.subplot(2, 4, 3)
plt.imshow(img_internet1)
plt.title("Image Internet 1")
plt.axis('off')

plt.subplot(2, 4, 4)
plt.imshow(img_internet2_resized)
plt.title("Image Internet 2")
plt.axis('off')

plt.subplot(2, 4, 8)
plt.imshow(sub_internet)
plt.title("Soustraction Internet")
plt.axis('off')

# Afficher le plot final
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
