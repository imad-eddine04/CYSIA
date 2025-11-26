a=int(input("donner un nombre: "))
b=int(input("donner un nombre: "))
def pgcd(a,b):
    if b==0:
        return a
    else:
        return pgcd(b,a%b)
if pgcd(a,b)==1:
    print("inverse de a egale : ",a%b)
else :
    print("inverse n'exist pas")


def factoriser_en_premiers(nombre):
    if nombre < 2:
        return []

    facteurs = []

    while nombre % 2 == 0:
        facteurs.append(2)
        nombre //= 2

    diviseur = 3
    while diviseur * diviseur <= nombre:
        while nombre % diviseur == 0:
            facteurs.append(diviseur)
            nombre //= diviseur

        diviseur += 2

    if nombre > 1:
        facteurs.append(nombre)

    return facteurs


# Exemple d'utilisation
nombre_a_factoriser = 1260
resultat = factoriser_en_premiers(nombre_a_factoriser)

print(resultat)