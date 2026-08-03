# src/solution.py

import hmac
import hashlib

def sign(key: bytes, message: bytes) -> str:
    if not key or not message:
        raise ValueError("Key and message must not be empty.")
    
    hmac_obj = hmac.new(key, message, hashlib.sha256)
    return hmac_obj.hexdigest()
