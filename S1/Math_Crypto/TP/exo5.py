a = int(input("Entrez un entier : "))
Tab = []
i = 2

while i <= a:
    if a % i == 0:
        Tab.append(i)
        a = a/i
    else:
        i = i+1

print("Facteurs premiers :", Tab)
