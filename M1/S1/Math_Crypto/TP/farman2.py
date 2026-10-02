import math

def fermat(a, p):
    if math.gcd(a, p) != 1:
        print(" test impossible")
    else:
        if pow(a, p - 1, p) == 1:
            print(f"Le théorème est vérifié pour a={a}, p={p}")
        else:
            print(f"Le théorème n’est pas vérifié pour a={a}, p={p}")

a = int(input("Donner a : "))
p = int(input("Donner p : "))
fermat(a, p)