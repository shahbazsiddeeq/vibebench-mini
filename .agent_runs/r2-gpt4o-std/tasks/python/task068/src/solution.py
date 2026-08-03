import hmac

def secure_compare(a: str, b: str) -> bool:
    """
    Compares two strings in constant time to prevent timing attacks.

    :param a: First string to compare.
    :param b: Second string to compare.
    :return: True if strings are equal, False otherwise.
    """
    # Convert strings to bytes to handle non-ASCII characters
    a_bytes = a.encode('utf-8')
    b_bytes = b.encode('utf-8')
    return hmac.compare_digest(a_bytes, b_bytes)
