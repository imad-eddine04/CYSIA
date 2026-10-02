
n = 77
e = 13
c = 10


p = 7
q = 11


phi = (p - 1) * (q - 1)


def modinv(a, m):
    for d in range(1, m):
        if (a * d) % m == 1:
            return d
    return None

d = modinv(e, phi)

m = pow(c, d, n)

print("p =", p)
print("q =", q)
print("phi =", phi)
print("d =", d)
print("Message déchiffré m =", m)