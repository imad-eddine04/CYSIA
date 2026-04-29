from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from Crypto.Cipher import AES
mohamed = ec . generate_private_key ( ec . SECP256R1 () )
ali = ec . generate_private_key ( ec . SECP256R1 () )
shared1 = mohamed . exchange ( ec . ECDH () , ali . public_key () )
shared2 = ali . exchange ( ec . ECDH () , mohamed . public_key () )
print ("Clés identiques :", shared1 == shared2 )
digest = hashes . Hash ( hashes . SHA256 () )
digest . update ( shared1 )
aes_key = digest . finalize ()
aes = AES . new ( aes_key , AES . MODE_EAX )
c , tag = aes . encrypt_and_digest ( b" Message ECC securise ")
print (" Chiffrement ECC+ AES ré ussi ")