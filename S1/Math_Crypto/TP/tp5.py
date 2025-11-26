from math import gcd

def phi(n):
    resultat = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            resultat -= resultat // p
        p += 1
    if n > 1:
        resultat -= resultat // n
    return resultat
n = int(input("Entrez un entier n : "))
print(f"φ({n}) = {phi(n)}")