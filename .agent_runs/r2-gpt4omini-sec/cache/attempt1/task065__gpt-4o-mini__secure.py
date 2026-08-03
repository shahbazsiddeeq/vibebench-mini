import base64

def b64_encode(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise TypeError("Input must be of type bytes.")
    return base64.b64encode(data).decode('utf-8')

def b64_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("Input must be of type str.")
    try:
        return base64.b64decode(s.encode('utf-8'))
    except (base64.binascii.Error, ValueError) as e:
        raise ValueError("Invalid base64 input.") from e
