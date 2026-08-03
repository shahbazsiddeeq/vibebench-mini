import hashlib
import hmac


def sign(key, message):
    """
    Returns the HMAC-SHA256 signature of message under key as a lowercase hex string.
    
    Args:
        key: bytes - the secret key
        message: bytes - the message to sign
        
    Returns:
        str - lowercase hex string of the HMAC-SHA256 signature
        
    Raises:
        ValueError: if key or message is empty
    """
    if not key or not message:
        raise ValueError("key and message must not be empty")
    
    signature = hmac.new(key, message, hashlib.sha256).hexdigest()
    return signature
