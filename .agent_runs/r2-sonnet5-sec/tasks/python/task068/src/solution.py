"""
Constant-Time String Comparison

Provides secure_compare(a, b) which compares two strings for equality
using a constant-time algorithm (hmac.compare_digest) to help prevent
timing attacks that could otherwise leak information about how many
leading characters of a secret match an attacker-supplied guess.

Only the standard library is used.
"""

import hmac


def secure_compare(a: str, b: str) -> bool:
    """
    Compare two strings for equality in constant time.

    Args:
        a: First string to compare.
        b: Second string to compare.

    Returns:
        True if the strings are equal, False otherwise (including when
        inputs are not strings or of different lengths).

    Notes:
        - Uses hmac.compare_digest, which performs the comparison in a
          way that does not leak timing information about where the
          first differing character occurs.
        - Strings are encoded to UTF-8 bytes before comparison so that
          non-ASCII characters are handled safely and deterministically.
        - Input validation ensures that unexpected types do not raise
          exceptions that could expose internal details; instead False
          is returned for any invalid input.
    """
    # Validate input types strictly; do not attempt implicit conversion
    # to avoid masking bugs or accepting unexpected types silently.
    if not isinstance(a, str) or not isinstance(b, str):
        return False

    try:
        a_bytes = a.encode("utf-8")
        b_bytes = b.encode("utf-8")
    except Exception:
        # Never expose internal error details; treat any encoding
        # failure as a comparison failure.
        return False

    # hmac.compare_digest handles differing lengths safely and in
    # constant time relative to the length of the inputs, without
    # branching based on the position of the first mismatch.
    return hmac.compare_digest(a_bytes, b_bytes)
