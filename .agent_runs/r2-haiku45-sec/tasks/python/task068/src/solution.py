import hmac


def secure_compare(a, b):
    """
    Compare two strings using constant-time comparison to prevent timing attacks.
    
    Uses hmac.compare_digest which takes the same amount of time regardless of
    where the strings differ, preventing attackers from inferring information
    through timing analysis.
    
    Args:
        a: First string to compare
        b: Second string to compare

    Returns:
        bool: True if strings are equal, False otherwise

    Raises:
        TypeError: If inputs are not strings
    """
    # Validate inputs are strings
    if not isinstance(a, str):
        raise TypeError(f"First argument must be a string, got {type(a).__name__}")
    if not isinstance(b, str):
        raise TypeError(f"Second argument must be a string, got {type(b).__name__}")

    # Encode strings to bytes for comparison
    # hmac.compare_digest requires bytes for non-ASCII strings
    a_bytes = a.encode('utf-8')
    b_bytes = b.encode('utf-8')
    
    # Use hmac.compare_digest for constant-time comparison
    # This prevents timing attacks by taking the same amount of time
    # regardless of where the strings differ
    return hmac.compare_digest(a_bytes, b_bytes)
