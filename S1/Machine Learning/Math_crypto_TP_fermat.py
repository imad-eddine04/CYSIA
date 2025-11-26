from math import gcd

a = int(input("enter a : "))
p = int(input("enter un nmbr premier p : "))

if gcd(a,p) == 1:

    if pow(a, p-1, p) == 1:
        print("le théoréme de fermat est vérifié ")
    else:
        print("le théoréme de fermat est pas vérifier ")
else:
    print("les nombres ne sont pas premier entre eux (pgcd(a, p) != 1")

"""try a=2 , p=9"""