from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from binascii import hexlify

K = b'0123456789abcdef'  # convertir la clé en bytes
cipher = AES.new(K, AES.MODE_ECB)

# Original Message
M1 = K
M2 = K
Cm0 = cipher.encrypt(b'\0' * AES.block_size)  # convertir la chaîne en bytes
Cm1 = cipher.encrypt(strxor(Cm0,M1))
Tm = Cm2 = cipher.encrypt(strxor(Cm1,M2))


N1 = b'iheiowehfiowehfw'  # convertir la chaîne en bytes

# Inject second message after the first message
Cx0 = cipher.encrypt(b'\0' * AES.block_size)  # convertir la chaîne en bytes
Cx1 = cipher.encrypt(strxor(Cx0,M1))
Cx2 = cipher.encrypt(strxor(Cx1,N1))
print(cipher.decrypt(Cx1))
# X needs to *encrypt* to the same value as Cm1
X = strxor(cipher.decrypt(Cx1),Cx2)
print(X)
Cx3 = cipher.encrypt(strxor(Cx2,X))
Tx = Cx4 = cipher.encrypt(strxor(Cx3,M2))

print("Tm = '%s'" % hexlify(Tm))
print("Tx = '%s'" % hexlify(Tx))
