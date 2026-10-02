# S-Box definition from the document
S_BOX = {
    0x0: 0xc, 0x1: 0x5, 0x2: 0x6, 0x3: 0xb,
    0x4: 0x9, 0x5: 0x0, 0x6: 0xa, 0x7: 0xd,
    0x8: 0x3, 0x9: 0xe, 0xa: 0xf, 0xb: 0x8,
    0xc: 0x4, 0xd: 0x7, 0xe: 0x1, 0xf: 0x2
}


def round_func(state, round_key):
    """
    Applies one round of the simplified cipher: XOR with key, then S-Box substitution.
    """
    state = state ^ round_key
    state = S_BOX[state]
    return state


def enc(block, key):
    """
    Encrypts a 4-bit block using the simplified 2-round cipher.

    Args:
        block (int): A 4-bit integer.
        key (int): An 8-bit integer key.

    Returns:
        int: The 4-bit encrypted block.
    """
    # Split 8-bit key into two 4-bit round keys
    k0 = key >> 4
    k1 = key & 0x0F

    # Round 1
    state = round_func(block, k0)

    # Round 2
    state = round_func(state, k1)

    return state


# --- Example for Exercise 1 ---
print("--- Exercise 1: Simplified Block Cipher ---")
plaintext_block = 0b1101  # Example 4-bit block (13)
key_8bit = 0b10100101  # Example 8-bit key (165)
encrypted_block = enc(plaintext_block, key_8bit)

print(f"Plaintext Block: {bin(plaintext_block)}")
print(f"Key: {bin(key_8bit)}")
print(f"Encrypted Block: {bin(encrypted_block)}")
print("-" * 20 + "\n")

