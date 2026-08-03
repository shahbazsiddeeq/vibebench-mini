def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using the Vigenere cipher with the given key.
    
    Args:
        plaintext: The text to encrypt
        key: The encryption key (ASCII letters only)
    
    Returns:
        The encrypted text
    
    Raises:
        TypeError: If plaintext or key is not a string
        ValueError: If key is empty or contains non-ASCII-letter characters
    """
    # Type validation
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a string")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Value validation for key
    if len(key) == 0:
        raise ValueError("key cannot be empty")
    
    for char in key:
        if not char.isascii() or not char.isalpha():
            raise ValueError("key must contain only ASCII letters")
    
    # Convert key to lowercase and get shifts
    key_lower = key.lower()
    key_shifts = [ord(c) - ord('a') for c in key_lower]
    
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha() and char.isascii():
            # Get the shift for this character
            shift = key_shifts[key_index % len(key_shifts)]
            key_index += 1
            
            if char.isupper():
                # Uppercase letter
                encrypted_char = chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                # Lowercase letter
                encrypted_char = chr((ord(char) - 97 + shift) % 26 + 97)
            
            result.append(encrypted_char)
        else:
            # Non-letter character, pass through unchanged
            result.append(char)
    
    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using the Vigenere cipher with the given key.
    
    Args:
        ciphertext: The text to decrypt
        key: The decryption key (ASCII letters only)
    
    Returns:
        The decrypted text
    
    Raises:
        TypeError: If ciphertext or key is not a string
        ValueError: If key is empty or contains non-ASCII-letter characters
    """
    # Type validation
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a string")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Value validation for key
    if len(key) == 0:
        raise ValueError("key cannot be empty")
    
    for char in key:
        if not char.isascii() or not char.isalpha():
            raise ValueError("key must contain only ASCII letters")
    
    # Convert key to lowercase and get shifts
    key_lower = key.lower()
    key_shifts = [ord(c) - ord('a') for c in key_lower]
    
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha() and char.isascii():
            # Get the shift for this character
            shift = key_shifts[key_index % len(key_shifts)]
            key_index += 1
            
            if char.isupper():
                # Uppercase letter
                decrypted_char = chr((ord(char) - 65 - shift) % 26 + 65)
            else:
                # Lowercase letter
                decrypted_char = chr((ord(char) - 97 - shift) % 26 + 97)
            
            result.append(decrypted_char)
        else:
            # Non-letter character, pass through unchanged
            result.append(char)
    
    return ''.join(result)
