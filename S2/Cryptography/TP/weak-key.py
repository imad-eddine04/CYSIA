from Crypto.Cipher import DES

key = bytes.fromhex("0101010101010101")
key1 = bytes.fromhex("01FE01FE01FE01FE")
key2 = bytes.fromhex("FE01FE01FE01FE01")
0
plaintext = b"Salamwra"

cipher = DES.new(key, DES.MODE_ECB)
ciphertext = cipher.encrypt(plaintext)

cipher2 = DES.new(key, DES.MODE_ECB)
double = cipher2.encrypt(ciphertext)

print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Double encryption:", double)
cipher1 = DES.new(key1, DES.MODE_ECB)
ciphertext = cipher1.encrypt(plaintext)

cipher2 = DES.new(key2, DES.MODE_ECB)
result = cipher2.encrypt(ciphertext)

print("Plaintext :", plaintext)
print("Ciphertext*semi :", ciphertext)
print("After second encryption :", result)