import hmac


def secure_compare(a, b):
    """
    Compare two strings using constant-time comparison to prevent timing attacks.

    Args:
        a: First string to compare
        b: Second string to compare

    Returns:
        True if strings are equal, False otherwise
    """
    return hmac.compare_digest(a.encode('utf-8'), b.encode('utf-8'))
