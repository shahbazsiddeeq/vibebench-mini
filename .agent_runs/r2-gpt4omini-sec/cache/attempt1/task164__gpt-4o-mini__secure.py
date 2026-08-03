# src/solution.py

def vigenere_encrypt(plaintext: str, key: str) -> str:
    if not isinstance(plaintext, str) or not isinstance(key, str):
        raise TypeError("Both plaintext and key must be strings.")
    if not key or any(not c.isalpha() for c in key):
        raise ValueError("Key must be a non-empty string containing only ASCII letters.")

    key = key.lower()
    key_length = len(key)
    key_index = 0
    ciphertext = []

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('a')
            if char.isupper():
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext.append(encrypted_char)
            key_index = (key_index + 1) % key_length
        else:
            ciphertext.append(char)

    return ''.join(ciphertext)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    if not isinstance(ciphertext, str) or not isinstance(key, str):
        raise TypeError("Both ciphertext and key must be strings.")
    if not key or any(not c.isalpha() for c in key):
        raise ValueError("Key must be a non-empty string containing only ASCII letters.")

    key = key.lower()
    key_length = len(key)
    key_index = 0
    plaintext = []

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('a')
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            plaintext.append(decrypted_char)
            key_index = (key_index + 1) % key_length
        else:
            plaintext.append(char)

    return ''.join(plaintext)
