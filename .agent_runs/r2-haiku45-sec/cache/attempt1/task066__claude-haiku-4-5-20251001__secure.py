def xor_cipher(data: bytes, key: bytes) -> bytes:
    """
    XORs each byte of data with the key byte at position i % len(key).
    
    Args:
        data: The bytes to encrypt/decrypt
        key: The key bytes (repeats cyclically)
        
    Returns:
        The XORed bytes
        
    Raises:
        ValueError: If key is empty
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if not isinstance(key, bytes):
        raise TypeError("key must be bytes")
    if len(key) == 0:
        raise ValueError("key cannot be empty")
    
    result = bytearray()
    for i, byte in enumerate(data):
        key_byte = key[i % len(key)]
        result.append(byte ^ key_byte)
    
    return bytes(result)
