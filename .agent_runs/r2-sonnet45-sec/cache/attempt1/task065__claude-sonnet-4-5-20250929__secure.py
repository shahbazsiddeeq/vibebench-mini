import base64
import binascii


def b64_encode(data: bytes) -> str:
    """
    Encodes bytes to base64 string.
    
    Args:
        data: bytes to encode
        
    Returns:
        base64 encoded string
        
    Raises:
        TypeError: if data is not bytes
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    
    return base64.b64encode(data).decode('ascii')


def b64_decode(s: str) -> bytes:
    """
    Decodes base64 string back to bytes.
    
    Args:
        s: base64 encoded string
        
    Returns:
        decoded bytes
        
    Raises:
        ValueError: if input is invalid base64
        TypeError: if s is not a string
    """
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    
    try:
        # Validate that the string contains only valid base64 characters
        # base64.b64decode will raise binascii.Error for invalid input
        return base64.b64decode(s, validate=True)
    except binascii.Error as e:
        raise ValueError(f"Invalid base64 input") from e
