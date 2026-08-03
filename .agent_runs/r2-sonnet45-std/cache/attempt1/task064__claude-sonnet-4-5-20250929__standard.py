import hmac
import hashlib


def sign(key: bytes, message: bytes) -> str:
    """
    Returns the HMAC-SHA256 signature of message under key as a lowercase hex string.
    
    Args:
        key: The secret key as bytes
        message: The message to sign as bytes
        
    Returns:
        The HMAC-SHA256 signature as a lowercase hex string
        
    Raises:
        ValueError: If key or message is empty
    """
    if not key:
        raise ValueError("Key cannot be empty")
    if not message:
        raise ValueError("Message cannot be empty")
    
    signature = hmac.new(key, message, hashlib.sha256).hexdigest()
    return signature
