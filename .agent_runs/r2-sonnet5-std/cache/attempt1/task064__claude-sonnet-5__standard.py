import hashlib
import hmac


def sign(key: bytes, message: bytes) -> str:
    if not key or not message:
        raise ValueError("key and message must be non-empty")
    return hmac.new(key, message, hashlib.sha256).hexdigest()
