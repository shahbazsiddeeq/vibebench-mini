import base64


def b64_encode(data: bytes) -> str:
    """Encodes bytes to base64 string."""
    return base64.b64encode(data).decode('ascii')


def b64_decode(s: str) -> bytes:
    """Decodes base64 string back to bytes. Raises ValueError on invalid input."""
    try:
        return base64.b64decode(s, validate=True)
    except Exception as e:
        raise ValueError(f"Invalid base64 input: {e}")
