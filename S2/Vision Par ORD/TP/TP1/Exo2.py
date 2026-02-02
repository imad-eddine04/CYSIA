from PIL import Image
MonImage = Image.open("tux.jpg")
print(MonImage.size) #on affiche la taille de l'image
print(MonImage.getpixel((45,40))) #on affiche l'information (R,G,B) du pixel decoordonnées (45,40)
bleu=(0,0,255)
red = (255,0,0)
MonImage.putpixel((20,20),bleu)
MonImage.putpixel((61,16),red)
MonImage.show() #On affiche l'image contenue dans la variable MonImage

#La taille de l'image de tux est : (64, 64)
#la couleur du pixel de coordonnées (45 ; 40) est (175, 170, 148)

