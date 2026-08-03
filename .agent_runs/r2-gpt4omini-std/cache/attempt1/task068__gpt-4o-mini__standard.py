# src/solution.py

import hmac

def secure_compare(a: str, b: str) -> bool:
    """Compares two strings in constant time to prevent timing attacks."""
    return hmac.compare_digest(a, b)
