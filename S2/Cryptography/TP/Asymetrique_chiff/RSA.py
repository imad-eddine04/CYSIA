from sympy import randprime , mod_inverse
from time import time
bits = 1024
p = randprime (2**( bits -1) , 2** bits )
q = randprime (2**( bits -1) , 2** bits )

n = p * q
phi = (p -1) *( q -1)
e = 65537
d = mod_inverse (e , phi )
print (" Taille de la clé RSA :", n . bit_length () , " bits ")
msg = int . from_bytes ( b" RSA_Test_Message ", 'big ')
c = pow( msg , e , n )
start = time ()
m = pow(c , d , n )
print ("Durée du dé chiffrement :", round ( time () - start , 3) , "s")
print (" Message clair :", m . to_bytes (( m . bit_length () +7) //8 , 'big ') )