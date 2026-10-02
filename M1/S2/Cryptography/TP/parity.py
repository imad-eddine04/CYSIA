from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from fractions import Fraction

# -----------------------------------------------------------
# 1. Clés RSA
# -----------------------------------------------------------
key = RSA.generate(1024)
n, e, d = key.n, key.e, key.d
print(f"[+] Module RSA : {n.bit_length()} bits")

# -----------------------------------------------------------
# 2. Message clair
# -----------------------------------------------------------
message = b"Secret_RSA_Parity"
m = bytes_to_long(message)
print(f"[+] Message clair (m) = {m}")

# -----------------------------------------------------------
# 3. Chiffrement
# -----------------------------------------------------------
c = pow(m, e, n)
print(f"[+] Chiffrement (c) = {c}")

# -----------------------------------------------------------
# 4. Oracle de parité
# -----------------------------------------------------------
def parity_oracle(cipher):
    return pow(cipher, d, n) % 2 == 0

print("[+] Oracle test :", "pair" if parity_oracle(c) else "impair")

# -----------------------------------------------------------
# 5. Attaque Parity Oracle (version exacte)
# -----------------------------------------------------------
low = Fraction(0, 1)
high = Fraction(n, 1)

c_attack = c
multiplier = pow(2, e, n)

print("\n[+] Début de l'attaque...\n")

for i in range(n.bit_length()):
    c_attack = (c_attack * multiplier) % n
    even = parity_oracle(c_attack)

    mid = (low + high) / 2

    if even:
        high = mid
    else:
        low = mid

    if i % 100 == 0 or i == n.bit_length() - 1:
        print(f"Étape {i:4d} → Intervalle ≈ {int(high - low)} valeurs")

# -----------------------------------------------------------
# 6. Récupération exacte du message
# -----------------------------------------------------------
m_rec = int(high)
message_rec = long_to_bytes(m_rec)

print("\n[+] Message retrouvé :", message_rec)
print("[+] Correspondance exacte ?", message_rec == message)
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

print("\n" + "="*60)
print("[+] SCÉNARIO 2 : RSA-OAEP (attaque impossible)")
print("="*60)

# -----------------------------------------------------------
# 7. Chiffrement RSA-OAEP
# -----------------------------------------------------------
cipher_oaep_enc = PKCS1_OAEP.new(key.publickey())
cipher_oaep_dec = PKCS1_OAEP.new(key)

ciphertext_oaep = cipher_oaep_enc.encrypt(message)

print("[+] Message clair        :", message)
print("[+] Chiffrement RSA-OAEP :", ciphertext_oaep.hex())
print("\n[+] Tentative de Parity Oracle Attack sur RSA-OAEP...\n")
def parity_oracle_oaep(ciphertext):
    try:
        m = cipher_oaep_dec.decrypt(ciphertext)
        return bytes_to_long(m) % 2 == 0
    except ValueError:
        # Padding OAEP invalide
        return None

low = Fraction(0, 1)
high = Fraction(n, 1)

c_attack = ciphertext_oaep
multiplier = pow(2, e, n)

for i in range(10):
    try:
        # Tentative artificielle : forcer une manipulation RSA
        c_int = bytes_to_long(c_attack)
        c_int = (c_int * multiplier) % n
        c_attack = long_to_bytes(c_int)

        result = parity_oracle_oaep(c_attack)

        if result is None:
            print(f"Étape {i:2d} → Padding OAEP invalide ❌")
            break

        print(f"Étape {i:2d} → Oracle =", "PAIR" if result else "IMPAIR")

    except Exception as ex:
        print(f"Erreur à l'étape {i}: {ex}")
        break
