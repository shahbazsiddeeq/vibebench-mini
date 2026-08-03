# src/solution.py

def xor_cipher(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("Key cannot be empty")
    
    key_length = len(key)
    result = bytearray(len(data))
    
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % key_length]
    
    return bytes(result)
