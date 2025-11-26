def pgcd(a, b):
    """Calcul du plus grand commun diviseur."""
    while b != 0:
        a, b = b, a % b
    return a

def phi(n):
    """Fonction indicatrice d’Euler."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def modinv(a, m):
    """Inverse modulaire de a mod m."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

p = 11
q = 3

n = p * q
phi = (p - 1) * (q - 1)

e = int(input("\nEntrez une valeur de e (premier avec phi) : "))

while pgcd(e, phi) != 1:
    e += 2

d = pow(e, -1, phi)

print("Clé publique  : (e =", e, ", n =", n, ")")
print("Clé privée   : (d =", d, ", n =", n, ")")

message = 9
print("\nMessage clair :", message)

c = pow(message, e, n)
print("Message chiffré :", c)

m = pow(c, d, n)
print("Message déchiffré :", m)