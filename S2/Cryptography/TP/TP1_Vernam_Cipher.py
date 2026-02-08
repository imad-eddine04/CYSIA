import numpy as np
def egcd (a , b ) :
    if a == 0:
        return b , 0 , 1
    else :
        gcd , x , y = egcd ( b % a , a )
        return gcd , y - ( b // a ) * x , x
def mod_inverse (a , m ) :
    gcd , x , y = egcd (a , m )
    if gcd != 1:
        raise ValueError (" Modular inverse does not exist ")
    return x % m

def matrix_mod_inverse ( matrix ) :
    det = int( np . round ( np . linalg . det ( matrix ) ) )
    det_inv = mod_inverse ( det , 2)
    matrix_minor = np . linalg . inv ( matrix ) . T * det
    matrix_adj = np . round ( matrix_minor ) . astype (int) % 2
    matrix_inv = ( det_inv * matrix_adj ) % 2
    return matrix_inv
#----------------------------------------------------------------------------

def vernam_encrypt_decrypt ( text , key ) :
    if len( text ) != len( key ) :
        raise ValueError ("Key must be the same length as the plaintext ")
    result = ''
    for char , k in zip ( text , key ) :
        result += chr(ord ( char ) ^ ord( k ) )
    return result



if __name__ == "__main__":
    text = "HELLO"
    key  = "XMCKL"

    encrypted = vernam_encrypt_decrypt(text, key)
    print("Original text :", text)
    print("Encrypted text:", encrypted)

    decrypted = vernam_encrypt_decrypt(encrypted, key)
    print("Decrypted text:", decrypted)
