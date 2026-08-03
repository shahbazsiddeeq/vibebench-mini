"""
A secure, self-contained implementation of the classic Vigenere cipher.

This module exposes two functions:

    vigenere_encrypt(plaintext: str, key: str) -> str
    vigenere_decrypt(ciphertext: str, key: str) -> str

Only ASCII alphabetic characters are transformed; every other character
(spaces, digits, punctuation, non-ASCII characters, etc.) is passed through
unchanged and does not consume a position in the repeating key.
"""

from __future__ import annotations

__all__ = ["vigenere_encrypt", "vigenere_decrypt"]


def _validate_inputs(text: object, key: object) -> None:
    """Validate the text and key arguments.

    Raises:
        TypeError: if `text` or `key` is not a str.
        ValueError: if `key` is empty or contains a non ASCII-letter char.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    if len(key) == 0:
        raise ValueError("key must not be empty")
    for ch in key:
        if not ("a" <= ch <= "z" or "A" <= ch <= "Z"):
            raise ValueError("key must contain only ASCII letters")


def _shifts(key: str) -> list:
    """Compute the list of shift values (0..25) for each key letter."""
    return [ord(ch.lower()) - ord("a") for ch in key]


def _transform(text: str, key: str, sign: int) -> str:
    """Apply the Vigenere transformation with the given sign (+1 encrypt, -1 decrypt)."""
    shifts = _shifts(key)
    key_len = len(shifts)
    key_index = 0
    out_chars = []

    for ch in text:
        if "A" <= ch <= "Z":
            shift = shifts[key_index % key_len]
            new_ord = (ord(ch) - ord("A") + sign * shift) % 26 + ord("A")
            out_chars.append(chr(new_ord))
            key_index += 1
        elif "a" <= ch <= "z":
            shift = shifts[key_index % key_len]
            new_ord = (ord(ch) - ord("a") + sign * shift) % 26 + ord("a")
            out_chars.append(chr(new_ord))
            key_index += 1
        else:
            out_chars.append(ch)

    return "".join(out_chars)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt `plaintext` using the Vigenere cipher with the given `key`.

    Args:
        plaintext: The text to encrypt.
        key: The cipher key; case-insensitive, ASCII letters only.

    Returns:
        The encrypted text.

    Raises:
        TypeError: if `plaintext` or `key` is not a str.
        ValueError: if `key` is empty or contains non ASCII-letter characters.
    """
    _validate_inputs(plaintext, key)
    return _transform(plaintext, key, sign=1)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt `ciphertext` using the Vigenere cipher with the given `key`.

    Args:
        ciphertext: The text to decrypt.
        key: The cipher key; case-insensitive, ASCII letters only.

    Returns:
        The decrypted text.

    Raises:
        TypeError: if `ciphertext` or `key` is not a str.
        ValueError: if `key` is empty or contains non ASCII-letter characters.
    """
    _validate_inputs(ciphertext, key)
    return _transform(ciphertext, key, sign=-1)
