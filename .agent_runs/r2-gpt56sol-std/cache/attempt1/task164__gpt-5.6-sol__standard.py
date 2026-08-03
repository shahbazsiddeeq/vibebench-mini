"""Vigenere cipher encryption and decryption utilities."""


def _validate(text: str, key: str) -> list[int]:
    """Validate arguments and return the key's numeric shifts."""
    if not isinstance(text, str) or not isinstance(key, str):
        raise TypeError("text and key must be strings")
    if not key or any(not ("A" <= char <= "Z" or "a" <= char <= "z") for char in key):
        raise ValueError("key must contain only ASCII letters and must not be empty")

    return [ord(char.lower()) - ord("a") for char in key]


def _transform(text: str, key: str, direction: int) -> str:
    shifts = _validate(text, key)
    output: list[str] = []
    key_position = 0

    for char in text:
        if "A" <= char <= "Z":
            base = ord("A")
        elif "a" <= char <= "z":
            base = ord("a")
        else:
            output.append(char)
            continue

        shift = shifts[key_position % len(shifts)] * direction
        output.append(chr((ord(char) - base + shift) % 26 + base))
        key_position += 1

    return "".join(output)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt plaintext using the classic Vigenere cipher."""
    return _transform(plaintext, key, 1)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using the classic Vigenere cipher."""
    return _transform(ciphertext, key, -1)
