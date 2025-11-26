
def pgcd(a,b):
    if b==0:
        return a
    else:
        return pgcd(b,a%b)

a=int(input("donner un nombre: "))
b=int(input("donner un nombre: "))
print("pgcd de ",a,"et",b,"est",pgcd(a,b))
