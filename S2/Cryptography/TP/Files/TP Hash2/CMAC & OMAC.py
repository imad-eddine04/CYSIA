from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad  # ✅ Import ajouté

BLOCK_SIZE = 16
Rb = 0x87

# === Dérivation des sous-clés CMAC (K1, K2) ===
def generate_subkeys(key):
    aes = AES.new(key, AES.MODE_ECB)
    block_size = 16
    L = aes.encrypt(b'\x00' * block_size)

    def shift_left(block):
        shifted = int.from_bytes(block, 'big') << 1
        shifted &= (1 << 128) - 1
        shifted = shifted.to_bytes(16, 'big')

        if block[0] & 0x80:  # MSB = 1
            shifted = strxor(shifted, b'\x00' * 15 + bytes([Rb]))

        return shifted

    K1 = shift_left(L)
    K2 = shift_left(K1)
    return K1, K2


# === Calcul du CMAC ===
def cmac(key, data):
    aes = AES.new(key, AES.MODE_ECB)
    block_size = 16
    K1, K2 = generate_subkeys(key)

    if len(data) == 0:
        n = 1
        flag = False
    else:
        n = (len(data) + block_size - 1) // block_size
        flag = (len(data) % block_size == 0)

    # Dernier bloc
    if flag:
        last_block = strxor(data[(n - 1) * block_size:n * block_size], K1)
    else:
        padded = pad(data[(n - 1) * block_size:n * block_size], block_size)
        last_block = strxor(padded, K2)

    # Initialisation
    X = b'\x00' * block_size
    for i in range(n - 1):
        block = data[i * block_size:(i + 1) * block_size]
        X = aes.encrypt(strxor(X, block))

    T = aes.encrypt(strxor(X, last_block))
    return T


# === Calcul du OMAC ===
def omac(key, message):
    aes = AES.new(key, AES.MODE_ECB)
    K1, _ = generate_subkeys(key)

    n = (len(message) + 15) // 16
    blocks = [message[i*16:(i+1)*16] for i in range(n)]

    if len(blocks[-1]) < 16:
        blocks[-1] += b'\x80' + b'\x00' * (15 - len(blocks[-1]))

    state = b'\x00' * 16
    for block in blocks[:-1]:
        state = aes.encrypt(strxor(state, block))

    last = strxor(blocks[-1], K1)
    return aes.encrypt(strxor(state, last))


# === Test ===
key = b'Sixteen byte key'
data = b'Master professional cyber security'

tag_cmac = cmac(key, data)
tag_omac = omac(key, data)

print("CMAC :", tag_cmac.hex())
print("OMAC :", tag_omac.hex())
