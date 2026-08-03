"""Constant-Time String Comparison module."""

import hmac


def secure_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to prevent timing attacks.

    Uses hmac.compare_digest which is designed to avoid timing side
    channels when comparing secret values (e.g., tokens, passwords).

    Args:
        a: First string to compare.
        b: Second string to compare.

    Returns:
        True if the strings are equal, False otherwise.
    """
    a_bytes = a.encode("utf-8")
    b_bytes = b.encode("utf-8")
    return hmac.compare_digest(a_bytes, b_bytes)
