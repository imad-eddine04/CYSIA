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


def caesar_encrypt ( text , shift ) :
    encrypted_text = ""
    for char in text :
        if char . isalpha () :
            shift_amount = 65 if char . isupper () else 97
            encrypted_text += chr (( ord( char ) - shift_amount + shift ) % 26 +
                 shift_amount )
        else :
            encrypted_text += char
    return encrypted_text
def caesar_decrypt ( text , shift ) :
    return caesar_encrypt ( text , - shift )



if __name__ == "__main__":
    text = "HELLO WORLD"
    shift = 3

    encrypted = caesar_encrypt(text, shift)
    print("Original text :", text)
    print("Encrypted text:", encrypted)

    decrypted = caesar_decrypt(encrypted, shift)
    print("Decrypted text:", decrypted)
