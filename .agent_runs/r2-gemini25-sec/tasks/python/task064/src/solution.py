import hmac
import hashlib

def sign(key: bytes, message: bytes) -> str:
    """
    Returns the HMAC-SHA256 signature of message under key as a lowercase hex string.

    Raises ValueError if key or message is empty.
    """
    if not key:
        raise ValueError("Key cannot be empty.")
    if not message:
        raise ValueError("Message cannot be empty.")

    # hmac.new handles various types of key and message, but we've already
    # validated them to be non-empty bytes.
    # The digestmod is set to hashlib.sha256.
    h = hmac.new(key, message, hashlib.sha256)
    return h.hexdigest()
