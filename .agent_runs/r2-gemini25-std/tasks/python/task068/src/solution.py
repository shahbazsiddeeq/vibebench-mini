import hmac

def secure_compare(a: str, b: str) -> bool:
    """
    Compares two strings in constant time using hmac.compare_digest to prevent timing attacks.

    Args:
        a: The first string to compare.
        b: The second string to compare.

    Returns:
        True if the strings are equal, False otherwise.
    """
    # hmac.compare_digest expects bytes-like objects.
    # Encode strings to bytes using a consistent encoding (e.g., 'utf-8').
    # This handles non-ASCII characters correctly.
    return hmac.compare_digest(a.encode('utf-8'), b.encode('utf-8'))
