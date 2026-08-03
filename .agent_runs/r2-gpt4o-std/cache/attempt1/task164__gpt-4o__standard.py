# src/solution.py

def vigenere_encrypt(plaintext: str, key: str) -> str:
    if not isinstance(plaintext, str) or not isinstance(key, str):
        raise TypeError("Both plaintext and key must be strings.")
    if not key.isalpha():
        raise ValueError("Key must consist only of ASCII letters.")
    if not key:
        raise ValueError("Key cannot be empty.")

    key = key.lower()
    key_length = len(key)
    ciphertext = []
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % key_length]) - ord('a')
            if char.islower():
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            ciphertext.append(new_char)
            key_index += 1
        else:
            ciphertext.append(char)

    return ''.join(ciphertext)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    if not isinstance(ciphertext, str) or not isinstance(key, str):
        raise TypeError("Both ciphertext and key must be strings.")
    if not key.isalpha():
        raise ValueError("Key must consist only of ASCII letters.")
    if not key:
        raise ValueError("Key cannot be empty.")

    key = key.lower()
    key_length = len(key)
    plaintext = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % key_length]) - ord('a')
            if char.islower():
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext.append(new_char)
            key_index += 1
        else:
            plaintext.append(char)

    return ''.join(plaintext)
