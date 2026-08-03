import base64
from typing import Union


def b64_encode(data: bytes) -> str:
    """
    Encode bytes to a base64 string.
    
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
    Decode a base64 string to bytes.
    
    Args:
        s: base64 encoded string
        
    Returns:
        decoded bytes
        
    Raises:
        ValueError: if the input is not valid base64
        TypeError: if s is not a string
    """
    if not isinstance(s, str):
        raise TypeError("input must be a string")
    
    try:
        return base64.b64decode(s, validate=True)
    except Exception as e:
        raise ValueError(f"invalid base64 input: {str(e)}") from e
