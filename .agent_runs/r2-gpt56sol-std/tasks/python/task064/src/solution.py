import hashlib
import hmac


def sign(key: bytes, message: bytes) -> str:
    """Return the lowercase hexadecimal HMAC-SHA256 signature."""
    if not key or not message:
        raise ValueError("key and message must not be empty")
    return hmac.new(key, message, hashlib.sha256).hexdigest()
