import base64
import binascii
import json


def decode_jwt_header(token):
    if not isinstance(token, str) or '.' not in token:
        raise ValueError("Invalid token: no '.' found")

    segment = token.split('.', 1)[0]

    padding_needed = (-len(segment)) % 4
    padded = segment + ('=' * padding_needed)

    try:
        decoded_bytes = base64.urlsafe_b64decode(padded)
    except (binascii.Error, ValueError):
        raise ValueError("Invalid base64url encoding in header segment")

    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Header segment is not valid UTF-8")

    try:
        header = json.loads(decoded_str)
    except (json.JSONDecodeError, ValueError):
        raise ValueError("Header segment is not valid JSON")

    if not isinstance(header, dict):
        raise ValueError("Decoded JSON header is not an object")

    return header
