import hmac

def secure_compare(a: str, b: str) -> bool:
    """
    Compares two strings in a constant-time manner to prevent timing attacks.

    Args:
        a: The first string to compare.
        b: The second string to compare.

    Returns:
        True if the strings are equal, False otherwise.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        # For security, we should not raise an error that might reveal type information
        # in a timing-sensitive context. Instead, treat non-string inputs as unequal.
        # However, hmac.compare_digest expects bytes-like objects.
        # If we strictly want to compare strings, we must encode them.
        # If inputs are not strings, they cannot be encoded to bytes,
        # so we'll treat them as unequal.
        return False

    # hmac.compare_digest requires bytes-like objects.
    # We must encode the strings to bytes. A consistent encoding like 'utf-8'
    # should be used.
    try:
        bytes_a = a.encode('utf-8')
        bytes_b = b.encode('utf-8')
    except UnicodeEncodeError:
        # If encoding fails for some reason (e.g., invalid characters for utf-8,
        # though unlikely for typical string inputs), treat as unequal.
        return False

    return hmac.compare_digest(bytes_a, bytes_b)
