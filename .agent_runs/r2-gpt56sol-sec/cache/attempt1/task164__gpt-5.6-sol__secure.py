"""Vigenere cipher implementation over the ASCII English alphabet."""

__all__ = ["vigenere_encrypt", "vigenere_decrypt"]


def _validate_inputs(text: str, key: str) -> tuple[int, ...]:
    """Validate arguments and return the key's numeric shifts."""
    if not isinstance(text, str) or not isinstance(key, str):
        raise TypeError("text and key must be strings")
    if not key:
        raise ValueError("key must not be empty")
    if any(not ("A" <= char <= "Z" or "a" <= char <= "z") for char in key):
        raise ValueError("key must contain only ASCII letters")

    return tuple(
        ord(char) - (65 if "A" <= char <= "Z" else 97)
        for char in key
    )


def _transform(text: str, key: str, direction: int) -> str:
    """Transform text using the Vigenere cipher in the given direction."""
    shifts = _validate_inputs(text, key)
    result: list[str] = []
    key_index = 0

    for char in text:
        code = ord(char)

        if 65 <= code <= 90:
            base = 65
        elif 97 <= code <= 122:
            base = 97
        else:
            result.append(char)
            continue

        shift = shifts[key_index % len(shifts)] * direction
        result.append(chr((code - base + shift) % 26 + base))
        key_index += 1

    return "".join(result)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt plaintext with a case-insensitive ASCII-letter Vigenere key."""
    return _transform(plaintext, key, 1)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext with a case-insensitive ASCII-letter Vigenere key."""
    return _transform(ciphertext, key, -1)
