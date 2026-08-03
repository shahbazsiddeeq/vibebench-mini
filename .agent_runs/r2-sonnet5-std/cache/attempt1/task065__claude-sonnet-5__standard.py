import base64
import binascii


def b64_encode(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    return base64.b64encode(data).decode("ascii")


def b64_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("s must be str")
    try:
        # validate=True ensures invalid characters raise an error
        return base64.b64decode(s, validate=True)
    except (binascii.Error, ValueError) as e:
        raise ValueError(f"Invalid base64 input: {e}")
