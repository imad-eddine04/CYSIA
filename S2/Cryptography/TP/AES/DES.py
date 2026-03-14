from Crypto . Cipher import DES
from Crypto . Util . Padding import pad , unpad
key = b'8 bytekey '
cipher = DES . new ( key , DES . MODE_ECB )
plaintext = b'SalutDES '
ciphertext = cipher . encrypt ( pad ( plaintext , DES . block_size ) )
print (" Texte chiffr é :", ciphertext )
decrypted = unpad ( cipher . decrypt ( ciphertext ) , DES . block_size )
print (" Texte dé chiffr é :", decrypted )
