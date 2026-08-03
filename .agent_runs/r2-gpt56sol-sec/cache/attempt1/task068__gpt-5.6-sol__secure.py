"""Security utilities for constant-time string comparison."""

import hmac


def secure_compare(a: str, b: str) -> bool:
    """Return whether two strings are equal using constant-time comparison."""
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("secure_compare arguments must be strings")

    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))
