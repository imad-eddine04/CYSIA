import math
import time


def factorisation(n):
    start_time = time.perf_counter()

    if n <= 1:
        end_time = time.perf_counter()
        temps_execution = end_time - start_time
        return None, None, temps_execution

    limite = int(math.sqrt(n)) + 1

    p = None
    q = None

    for i in range(2, limite):
        if n % i == 0:
            p = i
            q = n // i
            break

    end_time = time.perf_counter()
    temps_execution = end_time - start_time

    if p is None:
        p, q = n, 1

    return p, q, temps_execution


n_rsa = 391
p, q, temps = factorisation(n_rsa)

verification = p * q == n_rsa

print(f"n = {n_rsa}")
print(f"Les facteurs premiers sont p = {p} et q = {q}")
print(f"Vérification : p * q = {p} * {q} = {p * q}")
print(f"p * q = n : {verification}")
print(f"\nTemps d'exécution de la factorisation : {temps:.6f} secondes")