import secrets , hashlib
from Crypto . Cipher import AES
p = 0xFFFFFFFB # petit nombre premier (TP uniquement )
g = 5
a = secrets . randbelow ( p )
b = secrets . randbelow ( p )
A = pow(g , a , p )
B = pow(g , b , p )
K_M = pow (B , a , p )
K_A = pow (A , b , p )
print ("Clé commune identique ?", K_M == K_A )
key = hashlib . sha256 (str( K_M ) . encode () ) . digest ()
aes = AES . new ( key , AES . MODE_EAX )
ciphertext , tag = aes . encrypt_and_digest ( b" Message secret partage ")
print (" Message chiffr é :", ciphertext )



