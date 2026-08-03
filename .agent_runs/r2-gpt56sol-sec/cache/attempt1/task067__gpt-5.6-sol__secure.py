"""Secure URL-safe token generation."""

import base64
import operator
import secrets
from typing import Any


def gen_token(n_bytes: int = 32) -> str:
    """Return an unpadded URL-safe Base64 token from secure random bytes.

    Args:
        n_bytes: Number of random bytes to encode. Must be at least 8.

    Raises:
        TypeError: If ``n_bytes`` is not an integer.
        ValueError: If ``n_bytes`` is less than 8.
    """
    if isinstance(n_bytes, bool):
        raise TypeError("n_bytes must be an integer")

    try:
        size = operator.index(n_bytes)
    except TypeError:
        raise TypeError("n_bytes must be an integer") from None

    if size < 8:
        raise ValueError("n_bytes must be at least 8")

    random_bytes = secrets.token_bytes(size)
    return base64.urlsafe_b64encode(random_bytes).rstrip(b"=").decode("ascii")
