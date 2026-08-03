"""
Secure Token Generator
======================

Provides `gen_token(n_bytes=32)` which returns a URL-safe, base64-encoded
representation of `n_bytes` bytes of cryptographically secure randomness.

Security notes:
- Uses `secrets.token_bytes` (CSPRNG) rather than `random`.
- Validates input type and range before use.
- No I/O, no eval/exec, no external dependencies.
- Errors raised are generic ValueError/TypeError with minimal, non-sensitive
  messages (no internal state or stack details exposed).
"""

import base64
import secrets

_MIN_BYTES = 8


def gen_token(n_bytes: int = 32) -> str:
    """
    Generate a secure, URL-safe token string.

    Args:
        n_bytes: Number of random bytes to generate (must be an int >= 8).

    Returns:
        A URL-safe base64-encoded string (padding stripped) representing
        `n_bytes` bytes of cryptographically secure random data. The
        resulting string length is exactly (4 * n_bytes + 2) // 3.

    Raises:
        TypeError: if n_bytes is not an integer.
        ValueError: if n_bytes < 8.
    """
    if isinstance(n_bytes, bool) or not isinstance(n_bytes, int):
        raise TypeError("n_bytes must be an integer")

    if n_bytes < _MIN_BYTES:
        raise ValueError(f"n_bytes must be >= {_MIN_BYTES}")

    raw = secrets.token_bytes(n_bytes)
    encoded = base64.urlsafe_b64encode(raw)
    token = encoded.rstrip(b"=").decode("ascii")

    return token
