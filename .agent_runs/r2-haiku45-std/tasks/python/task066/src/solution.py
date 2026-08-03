def xor_cipher(data, key):
    """
    XORs each byte of data with the key byte at position i % len(key).
    
    Args:
        data: bytes object to cipher
        key: bytes object to use as repeating key
        
    Returns:
        bytes object with XOR cipher applied
        
    Raises:
        ValueError: if key is empty
    """
    if not key:
        raise ValueError("key cannot be empty")
    
    result = bytearray()
    for i, byte in enumerate(data):
        key_byte = key[i % len(key)]
        result.append(byte ^ key_byte)
    
    return bytes(result)
