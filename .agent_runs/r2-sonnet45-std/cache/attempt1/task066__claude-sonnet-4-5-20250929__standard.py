def xor_cipher(data, key):
    """
    XOR cipher that XORs each byte of data with the key byte at position i % len(key).
    
    Args:
        data: bytes to be XORed
        key: bytes key (repeats cyclically)
    
    Returns:
        bytes: XORed result
    
    Raises:
        ValueError: if key is empty
    """
    if not key:
        raise ValueError("Key cannot be empty")
    
    result = bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))
    return result
