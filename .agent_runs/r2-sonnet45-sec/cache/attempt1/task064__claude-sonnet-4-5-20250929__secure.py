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
    # Validate inputs
    if not isinstance(key, bytes):
        raise TypeError("key must be bytes")
    if not isinstance(message, bytes):
        raise TypeError("message must be bytes")
    
    if len(key) == 0:
        raise ValueError("key cannot be empty")
    if len(message) == 0:
        raise ValueError("message cannot be empty")
    
    # Compute HMAC-SHA256
    h = hmac.new(key, message, hashlib.sha256)
    
    # Return as lowercase hex string
    return h.hexdigest()
