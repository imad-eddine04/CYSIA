from PIL import Image
img = Image.new("RGB", (600,500), "blue")
red = (255,0,0)
white = (255,255,255)

for i in range (200,400):
    for j in range (0,500):
        img.putpixel((i,j),white)

for i in range (400,600):
    for j in range (0,500):
        img.putpixel((i,j),red)

img.show()
