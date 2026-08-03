"""Utilities for applying a repeating-key XOR cipher."""


def xor_cipher(data: bytes, key: bytes) -> bytes:
    """XOR each byte in *data* with a cyclically repeating *key*."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if not isinstance(key, bytes):
        raise TypeError("key must be bytes")
    if not key:
        raise ValueError("key must not be empty")

    key_length = len(key)
    return bytes(value ^ key[index % key_length] for index, value in enumerate(data))
