# src/solution.py

def xor_cipher(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("Key must not be empty.")
    
    key_length = len(key)
    return bytes(data[i] ^ key[i % key_length] for i in range(len(data)))
