# src/solution.py

import hmac

def secure_compare(a: str, b: str) -> bool:
    # Validate inputs to ensure they are strings
    if not isinstance(a, str) or not isinstance(b, str):
        raise ValueError("Both inputs must be strings.")
    
    # Use hmac.compare_digest for constant-time comparison
    return hmac.compare_digest(a.encode('utf-8'), b.encode('utf-8'))
