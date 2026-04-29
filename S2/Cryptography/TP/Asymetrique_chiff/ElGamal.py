from random import randint
p = 0xFFFFFFFB
g = 5
x = randint (2 , p -2) # clé priv ée
y = pow(g , x , p ) # clé publique
m = 1234567
k = randint (2 , p -2)
a = pow(g , k , p )
b = ( m * pow (y , k , p ) ) % p
m_rec = ( b * pow (a , p -1 -x , p ) ) % p
print (" Message ré cupéré :", m_rec == m )