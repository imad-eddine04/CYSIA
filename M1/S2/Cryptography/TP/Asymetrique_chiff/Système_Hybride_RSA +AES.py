from Crypto . PublicKey import RSA
from Crypto . Cipher import AES , PKCS1_OAEP
import secrets
key = RSA . generate (2048)
public_key = key . publickey ()
aes_key = secrets . token_bytes (32)
data = b" Message long et confidentiel "
cipher_aes = AES . new ( aes_key , AES . MODE_EAX )
ciphertext , tag = cipher_aes . encrypt_and_digest ( data )
cipher_rsa = PKCS1_OAEP . new ( public_key )
enc_aes_key = cipher_rsa . encrypt ( aes_key )
print ("Clé AES chiffr ée ( octets ) :", len( enc_aes_key ) )