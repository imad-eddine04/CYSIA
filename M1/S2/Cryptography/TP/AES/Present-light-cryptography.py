# ==========================================
#   PRESENT Lightweight Block Cipher (80-bit key)
# ==========================================

# S-Box
S = [0xC, 0x5, 0x6, 0xB,
     0x9, 0x0, 0xA, 0xD,
     0x3, 0xE, 0xF, 0x8,
     0x4, 0x7, 0x1, 0x2]

# Inverse S-Box
INV_S = [0x5, 0xE, 0xF, 0x8,
         0xC, 0x1, 0x2, 0xD,
         0xB, 0x4, 0x6, 0x3,
         0x0, 0x7, 0x9, 0xA]

# Permutation table
P = [
    0,16,32,48,1,17,33,49,2,18,34,50,3,19,35,51,
    4,20,36,52,5,21,37,53,6,22,38,54,7,23,39,55,
    8,24,40,56,9,25,41,57,10,26,42,58,11,27,43,59,
    12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63
]

# ==========================================
# Conversion helpers
# ==========================================

def hex_to_int(hex_string):
    return int(hex_string, 16)

def int_to_hex(value):
    return f"{value:016x}"

# ==========================================
# Permutation
# ==========================================

def permute(state):
    result = 0
    for i in range(64):
        bit = (state >> (63 - i)) & 1
        result |= bit << (63 - P[i])
    return result

def inverse_permute(state):
    result = 0
    for i in range(64):
        result <<= 1
        bit_position = 63 - P[i]
        result |= (state >> bit_position) & 1
    return result

# ==========================================
# Key schedule (80-bit key)
# ==========================================

def generate_subkeys(key_hex):
    key = int(key_hex, 16)
    subkeys = []

    for round_counter in range(1, 33):
        # Extract 64 MSB as subkey
        subkeys.append(key >> 16)

        # Rotate left 61 bits (80-bit rotation)
        key = ((key & (2**80 - 1)) << 61 | key >> 19) & (2**80 - 1)

        # Apply SBox to MSB nibble
        ms_nibble = (key >> 76) & 0xF
        key &= ~(0xF << 76)
        key |= S[ms_nibble] << 76

        # XOR round counter with bits k19..k15
        key ^= round_counter << 15

    return subkeys

# ==========================================
# Encryption
# ==========================================

def encrypt(plaintext_hex, key_hex):
    state = hex_to_int(plaintext_hex)
    subkeys = generate_subkeys(key_hex)

    for i in range(31):
        state ^= subkeys[i]

        # SBox layer
        new_state = 0
        for j in range(16):
            nibble = (state >> (j * 4)) & 0xF
            new_state |= S[nibble] << (j * 4)
        state = new_state

        # Permutation layer
        state = permute(state)

    # Final round key
    state ^= subkeys[31]

    return int_to_hex(state)

# ==========================================
# Decryption
# ==========================================

def decrypt(ciphertext_hex, key_hex):
    state = hex_to_int(ciphertext_hex)
    subkeys = generate_subkeys(key_hex)

    for i in range(31):
        state ^= subkeys[31 - i]
        state = inverse_permute(state)

        new_state = 0
        for j in range(16):
            nibble = (state >> (j * 4)) & 0xF
            new_state |= INV_S[nibble] << (j * 4)
        state = new_state

    state ^= subkeys[0]

    return int_to_hex(state)

# ==========================================
# Test
# ==========================================

if __name__ == "__main__":
    plaintext = input("Enter 64-bit plaintext (hex): ")
    key = input("Enter 80-bit key (hex): ")

    ciphertext = encrypt(plaintext, key)
    print("Ciphertext:", ciphertext)

    decrypted = decrypt(ciphertext, key)
    print("Decrypted:", decrypted)