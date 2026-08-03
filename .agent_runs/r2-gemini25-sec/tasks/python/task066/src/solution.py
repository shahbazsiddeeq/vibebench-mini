def xor_cipher(data: bytes, key: bytes) -> bytes:
    """
    XORs each byte of data with the key byte at position i % len(key),
    so a multi-byte key repeats cyclically.

    Raises ValueError if key is empty.
    Applying twice with the same key recovers the original data.

    Note: repeating-key XOR is not cryptographically secure and is for exercise use only.

    Args:
        data: The bytes object to be encrypted or decrypted.
        key: The bytes object representing the key.

    Returns:
        A new bytes object containing the XORed data.

    Raises:
        ValueError: If the key is empty.
        TypeError: If data or key are not bytes objects.
    """
    if not isinstance(data, bytes):
        raise TypeError("Data must be a bytes object.")
    if not isinstance(key, bytes):
        raise TypeError("Key must be a bytes object.")

    if not key:
        raise ValueError("Key cannot be empty.")

    result = bytearray(len(data))
    key_len = len(key)

    for i in range(len(data)):
        result[i] = data[i] ^ key[i % key_len]

    return bytes(result)
