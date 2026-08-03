# src/solution.py

import hmac

def secure_compare(a: str, b: str) -> bool:
    """
    Compares two strings in constant time to prevent timing attacks.
    
    :param a: First string to compare.
    :param b: Second string to compare.
    :return: True if strings are equal, False otherwise.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        return False
    
    return hmac.compare_digest(a, b)
