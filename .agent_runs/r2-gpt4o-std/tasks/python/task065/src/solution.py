# src/solution.py

import base64

def b64_encode(data: bytes) -> str:
    """Encodes bytes to a base64 string."""
    return base64.b64encode(data).decode('ascii')

def b64_decode(s: str) -> bytes:
    """Decodes a base64 string back to bytes. Raises ValueError on invalid input."""
    try:
        return base64.b64decode(s, validate=True)
    except (base64.binascii.Error, ValueError):
        raise ValueError("Invalid base64 input")
