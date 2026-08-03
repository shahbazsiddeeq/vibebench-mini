import hashlib
import hmac

def sign(key: bytes, message: bytes) -> str:
    if not key or not message:
        raise ValueError("Key and message must not be empty.")
    
    signature = hmac.new(key, message, hashlib.sha256).hexdigest()
    return signature
