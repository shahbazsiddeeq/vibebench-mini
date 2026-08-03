import base64

def b64_encode(data: bytes) -> str:
    """
    Encodes bytes to a base64 string.

    Args:
        data: The bytes to encode.

    Returns:
        The base64 encoded string.
    """
    return base64.b64encode(data).decode('ascii')

def b64_decode(s: str) -> bytes:
    """
    Decodes a base64 string back to bytes.

    Args:
        s: The base64 string to decode.

    Returns:
        The decoded bytes.

    Raises:
        ValueError: If the input string is not valid base64.
    """
    try:
        return base64.b64decode(s, validate=True)
    except Exception as e:
        raise ValueError(f"Invalid base64 string: {e}")
