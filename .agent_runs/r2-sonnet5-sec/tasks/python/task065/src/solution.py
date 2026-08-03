"""
Base64 Encode/Decode module.

Provides:
    b64_encode(data: bytes) -> str
    b64_decode(s: str) -> bytes

Security considerations:
    - Strict input type validation (no implicit coercion).
    - Strict base64 decoding (no silent acceptance of malformed input).
    - No use of eval/exec, no external I/O, no leakage of internal
      exception details to callers (errors are normalized to ValueError
      with a generic message).
"""

import base64
import binascii

__all__ = ["b64_encode", "b64_decode"]


def b64_encode(data: bytes) -> str:
    """
    Encode bytes to a base64-encoded ASCII string.

    Args:
        data: The bytes to encode.

    Returns:
        A base64-encoded string. Returns "" for empty input.

    Raises:
        ValueError: If `data` is not a bytes-like object.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise ValueError("data must be bytes or bytearray")

    try:
        encoded = base64.b64encode(bytes(data))
    except Exception:
        # Do not leak internal exception details.
        raise ValueError("failed to encode data")

    return encoded.decode("ascii")


def b64_decode(s: str) -> bytes:
    """
    Decode a base64-encoded string to bytes.

    Args:
        s: The base64-encoded string to decode.

    Returns:
        The decoded bytes.

    Raises:
        ValueError: If `s` is not a string, contains invalid base64
            characters/padding, or cannot otherwise be decoded.
    """
    if not isinstance(s, str):
        raise ValueError("input must be a string")

    # Reject empty string early (valid base64 of "" is "" -> b""),
    # but we still allow it since it's a legitimate case.
    if s == "":
        return b""

    # Validate characters strictly: only base64 alphabet + padding allowed.
    valid_chars = set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789+/="
    )
    if any(ch not in valid_chars for ch in s):
        raise ValueError("invalid base64 input")

    # Length must be a multiple of 4 for standard base64 with padding.
    if len(s) % 4 != 0:
        raise ValueError("invalid base64 input length")

    try:
        decoded = base64.b64decode(s, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError("invalid base64 input")
    except Exception:
        # Catch-all to avoid leaking unexpected internal errors.
        raise ValueError("invalid base64 input")

    return decoded
