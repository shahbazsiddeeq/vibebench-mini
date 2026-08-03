"""Base64 encoding and decoding utilities."""

import base64
import binascii


def b64_encode(data: bytes) -> str:
    """Encode bytes as a Base64 ASCII string."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    return base64.b64encode(data).decode("ascii")


def b64_decode(s: str) -> bytes:
    """Decode a Base64 string, raising ValueError for invalid input."""
    if not isinstance(s, str):
        raise ValueError("input must be a string")

    try:
        encoded = s.encode("ascii")
        return base64.b64decode(encoded, validate=True)
    except (UnicodeEncodeError, binascii.Error) as exc:
        raise ValueError("invalid Base64 input") from exc
