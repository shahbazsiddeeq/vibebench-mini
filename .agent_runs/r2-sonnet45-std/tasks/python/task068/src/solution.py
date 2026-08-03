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
    # Convert strings to bytes to handle non-ASCII characters
    a_bytes = a.encode('utf-8')
    b_bytes = b.encode('utf-8')
    return hmac.compare_digest(a_bytes, b_bytes)
