from PIL import Image

def calc_moy(img):
    width, height = img.size
    total_sum = 0
    for i in range(width):
        for j in range(height):
            total_sum += img.getpixel((i, j))
    return total_sum / (width * height)

img = Image.open("img_ng.jpeg")

img_ng = img.convert("L")
width, height = img_ng.size

moy = calc_moy(img_ng)
print(f"The average grayscale level is: {moy}")

b_img = Image.new("L", (width, height))
for i in range(width):
    for j in range(height):
        if img_ng.getpixel((i, j)) >= moy:
            b_img.putpixel((i, j), 255)
        else:
            b_img.putpixel((i, j), 0)

b_img.show()