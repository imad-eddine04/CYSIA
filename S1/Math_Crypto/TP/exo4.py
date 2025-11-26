def factoriser(n):
    if n < 2:
        return []
    l=[]

    while n % 2 == 0:
      l.append(2)
      n //= 2
    diviseur = 3
    while diviseur * diviseur <= n:
        while n % diviseur == 0:
            l.append(diviseur)
            n //= diviseur

        diviseur += 2

    if n > 1:
        l.append(n)

    return l

a=int(input("donner un nombre: "))
print(factoriser(a))