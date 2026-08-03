# src/solution.py

def xor_cipher(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("Key must not be empty.")
    
    key_length = len(key)
    result = bytearray()

    for i, byte in enumerate(data):
        result.append(byte ^ key[i % key_length])

    return bytes(result)
