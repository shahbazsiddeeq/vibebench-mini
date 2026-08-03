"""Strict Base64 encoding and decoding utilities."""

import base64
import binascii


def b64_encode(data: bytes) -> str:
    """Encode bytes as a canonical ASCII Base64 string."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    return base64.b64encode(data).decode("ascii")


def b64_decode(s: str) -> bytes:
    """Decode a canonical Base64 string, raising ValueError if invalid."""
    if not isinstance(s, str):
        raise TypeError("s must be a string")

    try:
        encoded = s.encode("ascii")
        decoded = base64.b64decode(encoded, validate=True)
    except (UnicodeEncodeError, binascii.Error, ValueError) as exc:
        raise ValueError("invalid Base64 input") from None

    if base64.b64encode(decoded) != encoded:
        raise ValueError("invalid Base64 input")

    return decoded
