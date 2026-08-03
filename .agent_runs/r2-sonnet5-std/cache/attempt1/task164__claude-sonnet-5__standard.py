def _validate(text, key):
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    if not key or not key.isascii() or not key.isalpha():
        raise ValueError("key must be a non-empty string of ASCII letters")


def _shift_char(c, shift):
    if c.isupper():
        return chr((ord(c) - 65 + shift) % 26 + 65)
    else:
        return chr((ord(c) - 97 + shift) % 26 + 97)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    _validate(plaintext, key)
    key = key.lower()
    result = []
    key_index = 0
    for c in plaintext:
        if c.isascii() and c.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            result.append(_shift_char(c, shift))
            key_index += 1
        else:
            result.append(c)
    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    _validate(ciphertext, key)
    key = key.lower()
    result = []
    key_index = 0
    for c in ciphertext:
        if c.isascii() and c.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            result.append(_shift_char(c, -shift))
            key_index += 1
        else:
            result.append(c)
    return ''.join(result)
