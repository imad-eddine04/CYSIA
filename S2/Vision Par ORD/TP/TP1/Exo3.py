from PIL import Image
MonImage=Image.open("paysage.jpg")
Taille=MonImage.size # Taille = (Largeur de l'image, hauteur de l'image)
for i in range(Taille[0]): #On parcourt l'image selon la largeur
 for j in range(Taille[1]): #On parcourt l'image selon la hauteur
    R,G,B=MonImage.getpixel((i,j)) #le code R,G,B du pixel de l'image
    gris=(R+G+B)//3 #On fait la moyenne des trois composantes. le // permetd'avoir le quotient entier dans la division par trois
    MonImage.putpixel((i,j),(gris,gris,gris)) #On met le pixel de coordonnées (i;j) à lacouleur gris
MonImage.show()

R=14
G=212
B=177
newcolor=Image.new("RGB",(300,400),(R,G,B))
newgris=(R+G+B)//3
for i in range(150,300):
 for j in range(0,400):
    newcolor.putpixel((i,j),(newgris,newgris,newgris))

newcolor.show()