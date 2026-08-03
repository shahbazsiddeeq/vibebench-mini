def _validate_inputs(text: str, key: str):
    """
    Validates the input types and key content for Vigenere cipher functions.
    Raises TypeError or ValueError for invalid inputs.
    """
    if not isinstance(text, str):
        raise TypeError("text argument must be a str")
    if not isinstance(key, str):
        raise TypeError("key argument must be a str")
    if not key:
        raise ValueError("key cannot be empty")
    if not all(c.isalpha() for c in key):
        raise ValueError("key must contain only ASCII letters (a-z, A-Z)")


def _vigenere_transform(text: str, key: str, encrypt: bool) -> str:
    """
    Performs Vigenere encryption or decryption.
    """
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
    """
    return _vigenere_transform(plaintext, key, encrypt=True)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypts ciphertext using the Vigenere cipher.
    """
    return _vigenere_transform(ciphertext, key, encrypt=False)
