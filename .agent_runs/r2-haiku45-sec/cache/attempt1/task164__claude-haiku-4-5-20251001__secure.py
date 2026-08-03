"""Vigenere Cipher implementation using standard library only."""


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using the Vigenere cipher with the given key.
    
    Args:
        plaintext: The text to encrypt (must be str)
        key: The encryption key (must be str of ASCII letters only)
    
    Returns:
        The encrypted text with case preserved and non-letters unchanged
    
    Raises:
        TypeError: If plaintext or key is not a str
        ValueError: If key is empty or contains non-ASCII-letter characters
    """
    # Validate input types
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a str")
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    
    # Validate key
    if len(key) == 0:
        raise ValueError("key cannot be empty")
    
    # Check that key contains only ASCII letters
    for char in key:
        if not char.isascii() or not char.isalpha():
            raise ValueError("key must contain only ASCII letters (a-z, A-Z)")
    
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.isascii() and char.isalpha():
            # Get the shift value from the current key character
            key_char = key[key_index % len(key)].lower()
            shift = ord(key_char) - ord('a')
            
            # Apply shift based on case
            if char.isupper():
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            
            result.append(encrypted_char)
            key_index += 1
        else:
            # Non-letter characters pass through unchanged and don't advance key
            result.append(char)
    
    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using the Vigenere cipher with the given key.
    
    Args:
        ciphertext: The text to decrypt (must be str)
        key: The decryption key (must be str of ASCII letters only)
    
    Returns:
        The decrypted text with case preserved and non-letters unchanged
    
    Raises:
        TypeError: If ciphertext or key is not a str
        ValueError: If key is empty or contains non-ASCII-letter characters
    """
    # Validate input types
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a str")
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    
    # Validate key
    if len(key) == 0:
        raise ValueError("key cannot be empty")
    
    # Check that key contains only ASCII letters
    for char in key:
        if not char.isascii() or not char.isalpha():
            raise ValueError("key must contain only ASCII letters (a-z, A-Z)")
    
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isascii() and char.isalpha():
            # Get the shift value from the current key character
            key_char = key[key_index % len(key)].lower()
            shift = ord(key_char) - ord('a')
            
            # Apply reverse shift based on case
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            result.append(decrypted_char)
            key_index += 1
        else:
            # Non-letter characters pass through unchanged and don't advance key
            result.append(char)
    
    return ''.join(result)
