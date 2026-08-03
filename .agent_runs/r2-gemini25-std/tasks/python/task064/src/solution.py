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

    # hmac.new expects key and msg to be bytes-like objects
    # hashlib.sha256 is the digestmod
    signature = hmac.new(key, message, hashlib.sha256).hexdigest()
    return signature
