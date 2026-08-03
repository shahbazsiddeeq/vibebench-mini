"""
Simple XOR Cipher (exercise use only).

This module implements a repeating-key XOR cipher. NOTE: repeating-key
XOR is NOT cryptographically secure and must never be used to protect
real secrets. It is provided for educational/exercise purposes only.
"""

from typing import ByteString


def xor_cipher(data: bytes, key: bytes) -> bytes:
    """
    XOR each byte of `data` with the corresponding byte of `key`,
    cycling the key as needed.

    Args:
        data: The input bytes to transform.
        key: The (non-empty) key bytes used cyclically.

    Returns:
        A new bytes object with each byte XORed against the key.

    Raises:
        ValueError: If `key` is empty or if `data`/`key` are not
            valid bytes-like objects.
    """
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise ValueError("data must be a bytes-like object")
    if not isinstance(key, (bytes, bytearray, memoryview)):
        raise ValueError("key must be a bytes-like object")

    data_bytes = bytes(data)
    key_bytes = bytes(key)

    if len(key_bytes) == 0:
        raise ValueError("key must not be empty")

    key_len = len(key_bytes)
    result = bytearray(len(data_bytes))
    for i, b in enumerate(data_bytes):
        result[i] = b ^ key_bytes[i % key_len]

    return bytes(result)
