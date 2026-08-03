import base64


def b64_encode(data: bytes) -> str:
    """Encode bytes to base64 string."""
    return base64.b64encode(data).decode('ascii')


def b64_decode(s: str) -> bytes:
    """Decode base64 string to bytes. Raises ValueError on invalid input."""
    try:
        return base64.b64decode(s, validate=True)
    except Exception as e:
        raise ValueError(f"Invalid base64 input: {e}")
