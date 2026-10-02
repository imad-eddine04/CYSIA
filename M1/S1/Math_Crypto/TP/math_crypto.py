import random

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def random_prime_3_digits():
    while True:
        n = random.randint(100, 999)
        if is_prime(n):
            return n

num = int(input("Entrez un nombre pour tester la primalité : "))
if is_prime(num):
    print(num, "est un nombre premier.")
else:
    print(num, "n'est PAS un nombre premier.")

prime_3_digits = random_prime_3_digits()
print("Un nombre premier aléatoire à 3 chiffres est :", prime_3_digits)