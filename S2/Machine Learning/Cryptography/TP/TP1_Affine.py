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

def affine_encrypt ( text , a , b ) :
    cipher = ''
    for char in text :
        if char . isalpha () :
            offset = 65 if char . isupper () else 97
            cipher += chr ((( a * (ord( char ) - offset ) + b ) % 26) + offset )
        else :
            cipher += char
    return cipher
def affine_decrypt ( cipher , a , b ) :
    plain = ''
    a_inv = mod_inverse(a , 26) # Ensure 'a' is coprime to 26
    for char in cipher :
        if char . isalpha () :
            offset = 65 if char . isupper () else 97
            plain += chr ((( a_inv * (( ord( char ) - offset ) - b ) ) % 26) +
            offset )
        else :
            plain += char
    return plain



if __name__ == "__main__":
    text = "SECRET"
    a = 7
    b = 3

    encrypted = affine_encrypt(text, a, b)
    print("Original text :", text)
    print("Encrypted text:", encrypted)

    decrypted = affine_decrypt(encrypted, a, b)
    print("Decrypted text:", decrypted)