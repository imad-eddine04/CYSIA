from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'0123456789abcdef' #Clé 16 Octets
cypher = AES.new(key, AES.MODE_ECB)

plaintext = b'HassiImadEddie'
plaintext1 = b'Fatima'
padded = pad(plaintext, AES.block_size) #adding padding
padded1 = pad(plaintext1, AES.block_size) #adding padding

ciphertext = cypher.encrypt(padded)
ciphertext1 = cypher.encrypt(padded1)
print("Text chiffrer : ",ciphertext.hex()) #.hex() for the good format

decrypted = unpad(cypher.decrypt(ciphertext), AES.block_size) #decrypted
print("Text dechiffrer : ",decrypted)

print("another example : ")
print("houssmam cypher text : ", ciphertext1.hex())
decrypted1 = unpad(cypher.decrypt(ciphertext1), AES.block_size) #decrypted
print("houssmam uncyphered text : ", decrypted1)