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
    # Validate inputs are strings
    if not isinstance(a, str):
        raise TypeError("First argument must be a string")
    if not isinstance(b, str):
        raise TypeError("Second argument must be a string")
    
    # Encode strings to bytes to handle non-ASCII characters
    # Use UTF-8 encoding which supports all Unicode characters
    a_bytes = a.encode('utf-8')
    b_bytes = b.encode('utf-8')
    
    # Use hmac.compare_digest for constant-time comparison
    # This prevents timing attacks by always taking the same amount of time
    # regardless of where the strings differ
    return hmac.compare_digest(a_bytes, b_bytes)
