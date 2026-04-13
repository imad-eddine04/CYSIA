from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import secrets

# =====================================================
#  1. PARAMÈTRES GLOBAUX
# =====================================================

BLOCK_SIZE = 16
MOD = 2**128                 # Modulo cohérent avec un tag 128 bits

# Clés secrètes
key_hash = secrets.randbelow(MOD - 1) + 1   # clé du hachage universel
key_enc  = get_random_bytes(16)              # clé AES (PRF)

# =====================================================
# 2. HACHAGE UNIVERSEL POLYNOMIAL
# =====================================================

def universal_hash(msg, key, mod):
    """
    H_k(m) = (…((m1 * k + m2) * k + m3)… ) mod mod
    """
    h = 0
    for byte in msg:
        h = (h * key + byte) % mod
    return h

# =====================================================
#3. MASQUE PSEUDO-ALÉATOIRE (PRF via AES)
# =====================================================

def pseudorandom_mask(key, nonce, mod):
    """
    Génère un masque pseudo-aléatoire à partir d'AES.
    AES-ECB est utilisé ici uniquement comme PRF sur un seul bloc.
    """
    r = AES.new(key, AES.MODE_ECB).encrypt(nonce)
    return int.from_bytes(r, 'big') % mod

# =====================================================
# 4. GÉNÉRATION DU CW-MAC
# =====================================================

def cw_mac(key_hash, key_enc, msg):
    """
    CW-MAC :
    1 Hachage universel
    2️ Masquage pseudo-aléatoire
    3️ Tag = (h + r) mod 2^128
    """
    nonce = get_random_bytes(16)              # 🔁 Nonce UNIQUE
    h = universal_hash(msg, key_hash, MOD)
    r = pseudorandom_mask(key_enc, nonce, MOD)
    tag = (h + r) % MOD
    return nonce, tag.to_bytes(16, 'big')

# =====================================================
# 5. VÉRIFICATION DU CW-MAC
# =====================================================

def verify_cw_mac(key_hash, key_enc, nonce, msg, tag):
    """
    Recalcule le tag et compare.
    """
    h = universal_hash(msg, key_hash, MOD)
    r = pseudorandom_mask(key_enc, nonce, MOD)
    expected = (h + r) % MOD
    return tag == expected.to_bytes(16, 'big')

# =====================================================
#  6. DÉMONSTRATION
# =====================================================

if __name__ == "__main__":
    msg = b"This is a test message."

    nonce, tag = cw_mac(key_hash, key_enc, msg)

    print(" Message :", msg)
    print(" Nonce   :", nonce.hex())
    print("  Tag CW-MAC :", tag.hex())

    print("\n Vérification du MAC")
    if verify_cw_mac(key_hash, key_enc, nonce, msg, tag):
        print(" MAC valide — intégrité confirmée")
    else:
        print(" MAC invalide — message altéré")
