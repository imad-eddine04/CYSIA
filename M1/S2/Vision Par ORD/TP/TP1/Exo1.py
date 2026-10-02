from PIL import Image
img=Image.new("RGB",(300,400),"white")
bleu=(0,0,255)
for i in range(150,300):
 for j in range(0,400):
    img.putpixel((i,j),bleu)
img.save("image1.png","png")
img.show()
