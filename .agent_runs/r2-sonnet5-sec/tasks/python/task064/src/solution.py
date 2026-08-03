"""
Secure HMAC-SHA256 signing utility.

This module exposes a single function, `sign`, which computes the
HMAC-SHA256 signature of a message under a given key, returning the
result as a lowercase hexadecimal string.

Security considerations:
- Uses the standard library `hmac` and `hashlib` modules (no custom
  crypto implementations).
- Validates inputs strictly: both `key` and `message` must be non-empty
  `bytes`-like objects.
- Does not leak internal state or stack traces; raises clean,
  well-defined exceptions with generic messages.
- No use of `eval`/`exec`, no external I/O, no logging of sensitive
  data.
"""

import hashlib
import hmac

__all__ = ["sign"]


def _validate_bytes(value: bytes, name: str) -> bytes:
    """
    Validate that `value` is a non-empty bytes-like object.

    Accepts `bytes` or `bytearray`; converts `bytearray` to `bytes`.
    Raises ValueError for empty or invalid input, without exposing
    the actual value.
    """
    if isinstance(value, bytearray):
        value = bytes(value)

    if not isinstance(value, bytes):
        raise ValueError(f"{name} must be a bytes-like object")

    if len(value) == 0:
        raise ValueError(f"{name} must not be empty")

    return value


def sign(key: bytes, message: bytes) -> str:
    """
    Compute the HMAC-SHA256 signature of `message` under `key`.

    Args:
        key: Non-empty bytes used as the HMAC key.
        message: Non-empty bytes to be authenticated.

    Returns:
        A lowercase hexadecimal string representing the HMAC-SHA256
        digest.

    Raises:
        ValueError: If `key` or `message` is empty or not a valid
            bytes-like object.
    """
    safe_key = _validate_bytes(key, "key")
    safe_message = _validate_bytes(message, "message")

    digest = hmac.new(safe_key, safe_message, hashlib.sha256).hexdigest()
    return digest
