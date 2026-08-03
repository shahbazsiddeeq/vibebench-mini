def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using the Vigenere cipher with the given key.
    
    Args:
        plaintext: The text to encrypt (must be str)
        key: The encryption key (must be non-empty str containing only ASCII letters)
    
    Returns:
        The encrypted ciphertext
    
    Raises:
        TypeError: If plaintext or key is not a str
        ValueError: If key is empty or contains non-ASCII-letter characters
    """
    # Type validation
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a str")
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    
    # Key validation
    if not key:
        raise ValueError("key must not be empty")
    if not all(c.isalpha() and ord(c) < 128 for c in key):
        raise ValueError("key must contain only ASCII letters")
    
    # Normalize key to lowercase and compute shifts
    key_lower = key.lower()
    key_shifts = [ord(c) - ord('a') for c in key_lower]
    
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha() and ord(char) < 128:
            # Get the shift for this position
            shift = key_shifts[key_index % len(key_shifts)]
            
            if char.isupper():
                # Encrypt uppercase letter
                encrypted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # Encrypt lowercase letter
                encrypted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            
            result.append(encrypted)
            key_index += 1
        else:
            # Non-letter characters pass through unchanged
            result.append(char)
    
    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using the Vigenere cipher with the given key.
    
    Args:
        ciphertext: The text to decrypt (must be str)
        key: The decryption key (must be non-empty str containing only ASCII letters)
    
    Returns:
        The decrypted plaintext
    
    Raises:
        TypeError: If ciphertext or key is not a str
        ValueError: If key is empty or contains non-ASCII-letter characters
    """
    # Type validation
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a str")
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    
    # Key validation
    if not key:
        raise ValueError("key must not be empty")
    if not all(c.isalpha() and ord(c) < 128 for c in key):
        raise ValueError("key must contain only ASCII letters")
    
    # Normalize key to lowercase and compute shifts
    key_lower = key.lower()
    key_shifts = [ord(c) - ord('a') for c in key_lower]
    
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha() and ord(char) < 128:
            # Get the shift for this position
            shift = key_shifts[key_index % len(key_shifts)]
            
            if char.isupper():
                # Decrypt uppercase letter
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                # Decrypt lowercase letter
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            result.append(decrypted)
            key_index += 1
        else:
            # Non-letter characters pass through unchanged
            result.append(char)
    
    return ''.join(result)
