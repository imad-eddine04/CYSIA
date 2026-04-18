from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'0123456789abcdef' #Clé 16 Octets
cypher = AES.new(key, AES.MODE_ECB)

plaintext = b'HassiImadEddie'

padded = pad(plaintext, AES.block_size) #adding padding


ciphertext = cypher.encrypt(padded)

print("Text chiffrer : ",ciphertext.hex()) #.hex() for the good format

decrypted = unpad(cypher.decrypt(ciphertext), AES.block_size) #decrypted
print("Text dechiffrer : ",decrypted)




