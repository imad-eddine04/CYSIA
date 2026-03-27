import random
import time

# --- 1. Global Constants & Configuration ---
MASK = 0xFFFFFFFFFFFFFFFF  # Ensures all operations stay within 64 bits [1]
ROUNDS = 8
MIX_CONSTANT = 0xAAAAAAAAAAAAAAAA  # Constant for MIX_XOR operation [2]


# --- 2. Random Generation of S-Box & P-Box (Student Defined) ---
# We generate these once and treat them as fixed tables for the cipher logic.
def generate_tables():
    # S-Box: Shuffle 0-15 (for 4-bit nibbles) [1, 3]
    s_values = list(range(16))
    random.shuffle(s_values)
    sbox = {i: s_values[i] for i in range(16)}
    inv_sbox = {v: k for k, v in sbox.items()}

    # P-Box: Shuffle 0-63 (for 64-bit diffusion) [3, 4]
    pbox = list(range(64))
    random.shuffle(pbox)

    # Inverse P-Box: Required to reverse the random shuffle during decryption
    inv_pbox = * 64
    for i in range(64):
        inv_pbox[pbox[i]] = i

    return sbox, inv_sbox, pbox, inv_pbox


S_BOX, INV_S_BOX, P_BOX, INV_P_BOX = generate_tables()


# --- 3. Component Functions ---

def apply_sbox(state, box):
    """Processes the 64-bit block in 16 nibbles (4 bits each) [5]"""
    new_state = 0
    for i in range(16):
        nibble = (state >> (i * 4)) & 0xF
        new_state |= (box[nibble] << (i * 4))
    return new_state


def apply_pbox(state, table):
    """Rearranges bits to new positions to ensure diffusion [2]"""
    res = 0
    for i in range(64):
        bit = (state >> i) & 1
        res |= (bit << table[i])
    return res


def generate_subkeys(master_key):
    """Derives 8 subkeys using ROT and ADD as required by Project #11 [4]"""
    subkeys = []
    current_key = master_key
    for i in range(ROUNDS):
        # ROT: Circular left shift by 13 bits
        current_key = ((current_key << 13) | (current_key >> (64 - 13))) & MASK
        # ADD: Modular addition with a round constant
        current_key = (current_key + (i * 0x123456789ABCDEF0)) & MASK
        subkeys.append(current_key)
    return subkeys


# --- 4. Main Cipher Logic ---

def encrypt(plaintext, master_key):
    subkeys = generate_subkeys(master_key)
    state = plaintext
    for i in range(ROUNDS):
        # 1. ADD_KEY: Combine state and subkey using addition [2, 6]
        state = (state + subkeys[i]) & MASK
        # 2. S-Box Layer (Confusion) [1, 7]
        state = apply_sbox(state, S_BOX)
        # 3. P-Box Layer (Diffusion) [4, 7]
        state = apply_pbox(state, P_BOX)
        # 4. MIX_XOR Layer [2, 8]
        state ^= MIX_CONSTANT
    return state


def decrypt(ciphertext, master_key):
    subkeys = generate_subkeys(master_key)
    state = ciphertext
    for i in range(ROUNDS - 1, -1, -1):
        # Reverse operations in exact opposite order
        state ^= MIX_CONSTANT  # Reverse MIX_XOR (XOR is its own inverse)
        state = apply_pbox(state, INV_P_BOX)  # Reverse P-Box
        state = apply_sbox(state, INV_S_BOX)  # Reverse S-Box
        state = (state - subkeys[i]) & MASK  # Reverse ADD_KEY (Subtraction) [2]
    return state


# --- 5. Evaluation & Testing ---

if __name__ == "__main__":
    # Test Values
    my_plaintext = 0x0123456789ABCDEF
    my_key = 0xFEDCBA9876543210

    print("--- Project #11: Mini Block Cipher ---")
    print(f"Plaintext:  {hex(my_plaintext)}")
    print(f"Master Key: {hex(my_key)}")

    # 1. Functional Test
    cipher = encrypt(my_plaintext, my_key)
    print(f"Ciphertext: {hex(cipher)}")

    decoded = decrypt(cipher, my_key)
    print(f"Decrypted:  {hex(decoded)}")

    # 2. Time Evaluation (Metric #6) [7]
    start_time = time.perf_counter_ns()
    for _ in range(100):
        encrypt(my_plaintext, my_key)
        decrypt(cipher, my_key)
    end_time = time.perf_counter_ns()

    avg_time = (end_time - start_time) / 100
    print(f"\nAverage time for 100 operations: {avg_time:.2f} nanoseconds")