import hmac

def secure_compare(a: str, b: str) -> bool:
    """Compares two strings in constant time to prevent timing attacks."""
    # Convert strings to bytes using UTF-8 encoding
    a_bytes = a.encode('utf-8')
    b_bytes = b.encode('utf-8')
    
    # Use hmac.compare_digest for constant-time comparison
    return hmac.compare_digest(a_bytes, b_bytes)
