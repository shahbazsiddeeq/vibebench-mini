"""RFC 7617 HTTP Basic authentication header encode/decode utilities."""

import base64
import binascii


def encode_basic_auth(username: str, password: str) -> str:
    if ':' in username:
        raise ValueError("username must not contain ':'")
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode('utf-8')).decode('ascii')
    return f"Basic {encoded}"


def decode_basic_auth(header: str) -> tuple:
    if not isinstance(header, str):
        raise ValueError("header must be a string")

    parts = header.split(' ', 1)
    if len(parts) != 2:
        raise ValueError("Invalid header format")

    scheme, token = parts
    if scheme.lower() != 'basic':
        raise ValueError("Scheme must be 'Basic'")

    if not token:
        raise ValueError("Missing base64 token")

    try:
        decoded_bytes = base64.b64decode(token, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError("Invalid base64 encoding")

    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Invalid UTF-8 encoding")

    if ':' not in decoded_str:
        raise ValueError("Decoded credentials must contain ':'")

    username, password = decoded_str.split(':', 1)
    return (username, password)
