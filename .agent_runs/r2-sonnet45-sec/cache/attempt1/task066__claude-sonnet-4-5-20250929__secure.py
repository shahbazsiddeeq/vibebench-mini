def xor_cipher(data: bytes, key: bytes) -> bytes:
    """
    XOR each byte of data with the key byte at position i % len(key).
    
    Args:
        data: The data to encrypt/decrypt as bytes
        key: The key to use for XOR operation as bytes
        
    Returns:
        The XORed result as bytes
        
    Raises:
        ValueError: If key is empty
    """
    if not key:
        raise ValueError("Key cannot be empty")
    
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    
    if not isinstance(key, bytes):
        raise TypeError("Key must be bytes")
    
    result = bytearray()
    key_len = len(key)
    
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % key_len])
    
    return bytes(result)
