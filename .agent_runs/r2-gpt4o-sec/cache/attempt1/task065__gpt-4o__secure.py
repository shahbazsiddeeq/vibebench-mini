# src/solution.py

import base64
import re

def b64_encode(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise TypeError("Input must be of type bytes.")
    return base64.b64encode(data).decode('ascii')

def b64_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("Input must be of type str.")
    
    # Validate base64 string
    if not re.match(r'^[A-Za-z0-9+/]*={0,2}$', s):
        raise ValueError("Invalid base64 input.")
    
    try:
        return base64.b64decode(s, validate=True)
    except (base64.binascii.Error, ValueError):
        raise ValueError("Invalid base64 input.")
