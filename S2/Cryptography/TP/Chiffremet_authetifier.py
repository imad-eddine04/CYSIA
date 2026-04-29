from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# ─────────────────────────────────────────
# 1. Key & message setup
# ─────────────────────────────────────────
key = get_random_bytes(16)          # 128-bit key
message = b"Message secret AES-GCM"
aad     = b"header"                 # Associated Authenticated Data

# ─────────────────────────────────────────
# 2. Encryption
# ─────────────────────────────────────────
def encrypt(key, message, aad):
    cipher = AES.new(key, AES.MODE_GCM)
    cipher.update(aad)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return cipher.nonce, ciphertext, tag

# ─────────────────────────────────────────
# 3. Decryption
# ─────────────────────────────────────────
def decrypt(key, nonce, ciphertext, tag, aad):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(aad)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext
    except ValueError:
        return None

# ─────────────────────────────────────────
# 4. Tests
# ─────────────────────────────────────────

print("=" * 50)
print("TEST 1 — Normal encryption/decryption")
print("=" * 50)
nonce, ciphertext, tag = encrypt(key, message, aad)
plaintext = decrypt(key, nonce, ciphertext, tag, aad)
print(f"Ciphertext : {ciphertext.hex()}")
print(f"Tag        : {tag.hex()}")
print(f"Decrypted  : {plaintext}")

print("\n" + "=" * 50)
print("TEST 2 — Integrity: tampered ciphertext")
print("=" * 50)
bad = bytearray(ciphertext)
bad[0] ^= 1                         # Flip one bit
result = decrypt(key, nonce, bytes(bad), tag, aad)
print("Erreur detectee" if result is None else f"Decrypted: {result}")

print("\n" + "=" * 50)
print("TEST 3 — AAD tampered")
print("=" * 50)
result = decrypt(key, nonce, ciphertext, tag, b"wrong_header")
print("AAD modifie => echec du dechiffrement" if result is None else f"Decrypted: {result}")

print("\n" + "=" * 50)
print("TEST 4 — Same message, different nonces")
print("=" * 50)
n1, c1, _ = encrypt(key, message, aad)
n2, c2, _ = encrypt(key, message, aad)
print(f"c1 : {c1.hex()}")
print(f"c2 : {c2.hex()}")
print(f"c1 != c2 : {c1 != c2}")

print("\n" + "=" * 50)
print("TEST 5 — Nonce reuse vulnerability")
print("=" * 50)
fixed_nonce1 = get_random_bytes(12)
fixed_nonce2 = get_random_bytes(12)
msg1 = b"Hello World!!!!!"
msg2 = b"Secret Password!"

cipher1 = AES.new(key, AES.MODE_GCM, nonce=fixed_nonce1)
ct1, _ = cipher1.encrypt_and_digest(msg1)

cipher2 = AES.new(key, AES.MODE_GCM, nonce=fixed_nonce1)
ct2, _ = cipher2.encrypt_and_digest(msg2)
#tag : b2cc1ae0349b9f1c26c5813e51e43ec3
# XOR of ciphertexts = XOR of plaintexts (critical leak!)
xor_ct = bytes(a ^ b for a, b in zip(ct1, ct2))
xor_pt = bytes(a ^ b for a, b in zip(msg1, msg2))
print(f"XOR(ct1, ct2) : {xor_ct.hex()}")
print(f"XOR(pt1, pt2) : {xor_pt.hex()}")
print(f"They match (nonce reuse leaks XOR): {xor_ct == xor_pt}")