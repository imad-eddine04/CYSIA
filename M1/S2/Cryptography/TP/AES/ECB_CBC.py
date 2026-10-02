from PIL import Image
from Crypto . Cipher import AES
from Crypto . Util . Padding import pad
from Crypto . Random import get_random_bytes

key = b'0123456789abcdef'
img = Image.open ("Plane.png")
data = pad(img.tobytes(), AES.block_size)
# ECB
cipher_ecb = AES.new(key, AES.MODE_ECB)
enc_ecb = cipher_ecb.encrypt(data)
img_ecb = Image.frombytes(img.mode, img.size, enc_ecb[:len(img.tobytes())])
img_ecb.save("ecb.jpg")
# CBC
iv = get_random_bytes(16)
cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
enc_cbc = cipher_cbc.encrypt(data)
img_cbc = Image.frombytes(img.mode , img.size ,enc_cbc[:len(img.tobytes())])
img_cbc.save("cbc.jpg")