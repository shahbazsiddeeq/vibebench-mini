"""Simple repeating-key XOR cipher."""

from itertools import cycle


def xor_cipher(data: bytes, key: bytes) -> bytes:
    """XOR each byte of *data* with a cyclically repeating *key*."""
    if not key:
        raise ValueError("key must not be empty")
    return bytes(value ^ key_byte for value, key_byte in zip(data, cycle(key)))
