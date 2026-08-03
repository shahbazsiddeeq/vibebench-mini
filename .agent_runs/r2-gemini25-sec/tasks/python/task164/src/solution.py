import secrets

def _validate_inputs(text, key):
    if not isinstance(text, str):
        raise TypeError("text argument must be a str")
    if not isinstance(key, str):
        raise TypeError("key argument must be a str")
    if not key:
        raise ValueError("key cannot be empty")
    if not all('a' <= c.lower() <= 'z' for c in key):
        raise ValueError("key must contain only ASCII letters (a-z, A-Z)")

def _vigenere_cipher(text: str, key: str, encrypt: bool) -> str:
    _validate_inputs(text, key)

    result = []
    key_len = len(key)
    key_idx = 0

    for char in text:
        if 'a' <= char <= 'z':
            shift = ord(key[key_idx % key_len].lower()) - ord('a')
            if not encrypt:
                shift = -shift
            transformed_char_code = (ord(char) - ord('a') + shift) % 26 + ord('a')
            result.append(chr(transformed_char_code))
            key_idx += 1
        elif 'A' <= char <= 'Z':
            shift = ord(key[key_idx % key_len].lower()) - ord('a')
            if not encrypt:
                shift = -shift
            transformed_char_code = (ord(char) - ord('A') + shift) % 26 + ord('A')
            result.append(chr(transformed_char_code))
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)

def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypts plaintext using the Vigenere cipher.

    Args:
        plaintext: The text to encrypt.
        key: The encryption key, consisting only of ASCII letters.

    Returns:
        The encrypted ciphertext.

    Raises:
        TypeError: If plaintext or key is not a string.
        ValueError: If key is empty or contains non-ASCII-letter characters.
    """
    return _vigenere_cipher(plaintext, key, encrypt=True)

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypts ciphertext using the Vigenere cipher.

    Args:
        ciphertext: The text to decrypt.
        key: The decryption key, consisting only of ASCII letters.

    Returns:
        The decrypted plaintext.

    Raises:
        TypeError: If ciphertext or key is not a string.
        ValueError: If key is empty or contains non-ASCII-letter characters.
    """
    return _vigenere_cipher(ciphertext, key, encrypt=False)
