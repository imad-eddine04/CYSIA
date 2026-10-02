# 1. Simplified Block Cipher Core
S_BOX = {
    0: 12, 1: 5, 2: 6, 3: 11,
    4: 9, 5: 0, 6: 10, 7: 13,
    8: 3, 9: 14, 10: 15, 11: 8,
    12: 4, 13: 7, 14: 1, 15: 2
}

INV_S_BOX = {v: k for k, v in S_BOX.items()}

def s_box(n):
    return S_BOX[n]

def inv_s_box(n):
    return INV_S_BOX[n]

def round_function(state, key):
    k0, k1 = key
    state ^= k0
    state = s_box(state)
    state ^= k1
    state = s_box(state)
    return state

def back_round(state, key):
    k0, k1 = key
    state = inv_s_box(state)
    state ^= k1
    state = inv_s_box(state)
    state ^= k0
    return state

def enc(message, key):
    k0 = (key >> 4) & 0x0F
    k1 = key & 0x0F
    state = round_function(message, (k0, k1))
    state = round_function(state, (k0, k1))
    return state

def dec(ciphertext, key):
    k0 = (key >> 4) & 0x0F
    k1 = key & 0x0F
    state = back_round(ciphertext, (k0, k1))
    state = back_round(state, (k0, k1))
    return state

# 2. Byte-Level Encryption (Exercice 2)
def enc_byte(byte, key):
    """Chiffre un byte (8 bits) en le divisant en deux nibbles (4 bits)"""
    high = (byte >> 4) & 0x0F
    low = byte & 0x0F

    high_enc = enc(high, key)
    low_enc = enc(low, key)

    return (high_enc << 4) | low_enc


def dec_byte(byte, key):
    """Déchiffre un byte (8 bits) en le divisant en deux nibbles (4 bits)"""
    high = (byte >> 4) & 0x0F
    low = byte & 0x0F

    high_dec = dec(high, key)
    low_dec = dec(low, key)

    return (high_dec << 4) | low_dec


# 3. CBC Mode Implementation (Exercice 3)
def encrypt_file_cbc(plaintext_file, key, iv, ciphertext_file):
    """Chiffre un fichier en utilisant le mode CBC"""
    with open(plaintext_file, "rb") as f:
        data = f.read()
    
    previous = iv
    encrypted = bytearray()
    
    for byte in data:
        block = byte ^ previous
        cipher_block = enc_byte(block, key)
        encrypted.append(cipher_block)
        previous = cipher_block
    
    with open(ciphertext_file, "wb") as f:
        f.write(encrypted)


def decrypt_file_cbc(ciphertext_file, key, iv, decrypted_file):
    """Déchiffre un fichier chiffré en mode CBC"""
    with open(ciphertext_file, "rb") as f:
        data = f.read()
    
    previous = iv
    decrypted = bytearray()
    
    for byte in data:
        plain_block = dec_byte(byte, key) ^ previous
        decrypted.append(plain_block)
        previous = byte
        
    with open(decrypted_file, "wb") as f:
        f.write(decrypted)


# --- Section de test ---
if __name__ == "__main__":
    print("=" * 60)
    print("S-Box Cryptosystem - Complete Test Suite")
    print("=" * 60)
    
    # Test 1: Original 4-bit encryption
    print("\n--- Test 1: 4-bit Encryption ---")
    msg_original = 0xA
    ma_cle = 0x3F
    chiffre = enc(msg_original, ma_cle)
    clair = dec(chiffre, ma_cle)
    
    print(f"Message original : {hex(msg_original)} ({msg_original})")
    print(f"Clé utilisée     : {hex(ma_cle)}")
    print(f"Ciphertext       : {hex(chiffre)}")
    print(f"Message retrouvé : {hex(clair)}")
    print(f"Status: {'[SUCCESS]' if msg_original == clair else '[FAILED]'}")
    
    # Test 2: ASCII input test
    print("\n--- Test 2: ASCII Character Encryption (8-bit) ---")
    user_input = input("Enter a character (or press Enter for 'A'): ").strip()
    if not user_input:
        user_input = "A"
    
    char = user_input[0]
    ascii_value = ord(char)
    key = 0x3F
    
    encrypted = enc_byte(ascii_value, key)
    decrypted = dec_byte(encrypted, key)
    
    print(f"Character       : '{char}'")
    print(f"ASCII Value     : {ascii_value} ({hex(ascii_value)})")
    print(f"Encrypted       : {encrypted} ({hex(encrypted)})")
    print(f"Decrypted       : {decrypted} ({hex(decrypted)})")
    print(f"Character back  : '{chr(decrypted)}'")
    print(f"Status: {'[SUCCESS]' if decrypted == ascii_value else '[FAILED]'}")
    
    # Test 3: CBC Mode with File Encryption/Decryption
    print("\n--- Test 3: CBC Mode File Encryption/Decryption ---")
    
    # Create test file
    plaintext_filename = "plaintext.txt"
    ciphertext_filename = "ciphertext.bin"
    decrypted_filename = "decrypted.txt"
    
    # User input for test data
    user_text = input("Enter text to encrypt (or press Enter for 'Hello World'): ").strip()
    if not user_text:
        user_text = "Hello World"
    
    # Write plaintext to file
    with open(plaintext_filename, "w") as f:
        f.write(user_text)
    
    print(f"\nOriginal text written to '{plaintext_filename}':")
    print(f"  Content: '{user_text}'")
    print(f"  Size: {len(user_text)} bytes")
    
    # CBC Mode parameters
    key = 0x3F
    iv = 0x55  # Initialization Vector
    
    # Encrypt
    print(f"\nEncrypting with CBC mode (key={hex(key)}, IV={hex(iv)})...")
    encrypt_file_cbc(plaintext_filename, key, iv, ciphertext_filename)
    
    with open(ciphertext_filename, "rb") as f:
        ciphertext_data = f.read()
    print(f"Ciphertext written to '{ciphertext_filename}'")
    print(f"  Encrypted bytes: {' '.join(hex(b) for b in ciphertext_data)}")
    print(f"  Size: {len(ciphertext_data)} bytes")
    
    # Decrypt
    print(f"\nDecrypting with CBC mode...")
    decrypt_file_cbc(ciphertext_filename, key, iv, decrypted_filename)
    
    with open(decrypted_filename, "r") as f:
        decrypted_text = f.read()
    print(f"Plaintext recovered from '{decrypted_filename}':")
    print(f"  Content: '{decrypted_text}'")
    print(f"  Size: {len(decrypted_text)} bytes")
    
    # Verification
    if user_text == decrypted_text:
        print("\n[SUCCESS] CBC Mode Test: Decrypted text matches original!")
    else:
        print("\n[FAILED] CBC Mode Test: Decrypted text does NOT match!")
        print(f"  Expected: '{user_text}'")
        print(f"  Got:      '{decrypted_text}'")
    
    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)
