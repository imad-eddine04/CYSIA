import random

#Part 1: Global Constants and S-Box/P-Box
#We define the substitution and permutation tables first. We will use the 4-bit S-Box from your TP to process the 64-bit block in 16 small "nibbles"

# 1. 64-bit Mask to keep results within 64 bits
MASK = 0xFFFFFFFFFFFFFFFF

# --- 1. Random S-Box Generation ---
# An S-Box for 4-bit nibbles must contain a shuffle of numbers 0 to 15.
sbox_values = list(range(16))
random.shuffle(sbox_values)

# Convert to dictionary format as used in your TPs [5, 6]
S_BOX = {i: sbox_values[i] for i in range(16)}

# Generate the Inverse S-Box for decryption [3, 5]
INV_S_BOX = {v: k for k, v in S_BOX.items()}

# --- 2. Random P-Box Generation ---
# A P-Box for a 64-bit block must contain a shuffle of positions 0 to 63.
P_BOX = list(range(64))
random.shuffle(P_BOX)


# --- 3. Print the results for your report ---
print("Generated S_BOX:", S_BOX)
print("\nGenerated P_BOX:", P_BOX)

#Part 2: Key Scheduling (Key Expansion)
#You must derive 8 subkeys from one 64-bit master key using ADD and ROT operations

def generate_subkeys(master_key):
    subkeys = []
    current_key = master_key

    for i in range(8):
        # 1. ROT: Circular Left Shift by 13 bits
        # (x << n) moves bits left, (x >> (64-n)) wraps the overflow back to the start
        current_key = ((current_key << 13) | (current_key >> (64 - 13))) & MASK

        # 2. ADD: Modular addition with a round constant to make each key unique
        current_key = (current_key + (i * 0x123456789ABCDEF0)) & MASK

        subkeys.append(current_key)

    return subkeys

#Part 3: Round Component Functions
#These functions apply the S-Box and P-Box to the entire 64-bit state.

def apply_sbox(state, box):
    new_state = 0
    # Process the 64-bit block in 16 nibbles (4 bits each)
    for i in range(16):
        # Isolate 4 bits using a shift and a 0xF (1111) mask [3, 5]
        nibble = (state >> (i * 4)) & 0xF
        # Substitute the nibble
        substituted = box[nibble]
        # Put it back in its position
        new_state |= (substituted << (i * 4))
    return new_state


def apply_pbox(state):
    """
    Applies bit-level permutation to the 64-bit state using the P_BOX table.
    Ensures 'Diffusion' by rearranging bits to new positions [1, 6].
    """
    res = 0
    for i in range(64):
        # 1. Isolate the bit at the current position 'i'
        bit = (state >> i) & 1  # Using bitwise shift and AND mask [4, 5]

        # 2. Shift the isolated bit to its new position defined by the P_BOX
        # 3. Use OR (|) to place it in the resulting state
        res |= (bit << P_BOX[i])

    return res


#Part 4: The Round Function
#This combines your assigned operations: ADD_KEY, S-Box, P-Box, and MIX_XOR

def round_function(state, round_key):
    # 1. ADD_KEY: Mix state with key using addition [1, 12]
    state = (state + round_key) & MASK

    # 2. Substitution Layer
    state = apply_sbox(state, S_BOX)

    # 3. Permutation Layer
    state = apply_pbox(state)

    # 4. MIX_XOR: Mix with a constant to increase randomness [1, 8]
    state ^= 0xAAAAAAAAAAAAAAA  # Assigned Mix Function: MIX_XOR

    return state

#Part 5: Full Encryption and Decryption
#Finally, we loop through the 8 rounds


def encrypt(plaintext, master_key):
    subkeys = generate_subkeys(master_key)
    state = plaintext

    for i in range(8):
        state = round_function(state, subkeys[i])

    return state


def decrypt(ciphertext, master_key):
    subkeys = generate_subkeys(master_key)
    state = ciphertext

    # In decryption, we apply rounds in reverse order [5, 14]
    for i in range(7, -1, -1):
        # 1. Reverse MIX_XOR (XOR is its own inverse)
        state ^= 0xAAAAAAAAAAAAAAA

        # 2. Reverse P-Box (Since our P-Box is its own inverse)
        state = apply_pbox(state)

        # 3. Reverse S-Box
        state = apply_sbox(state, INV_S_BOX)

        # 4. Reverse ADD_KEY (Subtraction reverses Addition)
        state = (state - subkeys[i]) & MASK

    return state


if __name__ == "__main__":
    # Test values (64-bit integers)
    my_plaintext = 0x0123456789ABCDEF
    my_key = 0xFEDCBA9876543210

    print(f"--- Project #11 Test Run ---")
    print(f"Original Plaintext: {hex(my_plaintext)}")

    # Encrypt
    cipher_text = encrypt(my_plaintext, my_key)
    print(f"Ciphertext:         {hex(cipher_text)}")

    # Decrypt
    decrypted_text = decrypt(cipher_text, my_key)
    print(f"Decrypted Result:   {hex(decrypted_text)}")

    if my_plaintext == decrypted_text:
        print("\nSUCCESS: The decryption perfectly matches the original!")
    else:
        print("\nFAILURE: The decryption does not match.")