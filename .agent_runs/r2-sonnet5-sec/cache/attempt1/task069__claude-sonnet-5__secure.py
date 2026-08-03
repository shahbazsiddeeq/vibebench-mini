"""
src/solution.py

Provides decode_jwt_header(token): decode (without verifying) the header
segment of a JWT token.
"""

import base64
import binascii
import json


def decode_jwt_header(token):
    """
    Decode and return the header of a JWT token as a dict.

    The header is the first '.'-separated segment of the token, base64url
    encoded (without padding). This function re-adds the required padding,
    decodes it, parses it as JSON, and ensures the result is a JSON object.

    No signature verification is performed.

    Raises:
        ValueError: if the token has no '.', the header segment is not
            valid base64url, the decoded content is not valid JSON, or
            the decoded JSON is not an object (dict).
    """
    if not isinstance(token, str):
        raise ValueError("Invalid token")

    if "." not in token:
        raise ValueError("Invalid token: missing '.' separator")

    header_segment = token.split(".", 1)[0]

    if not header_segment:
        raise ValueError("Invalid token: empty header segment")

    # base64url decoding requires padding to a multiple of 4 characters
    padding_needed = (-len(header_segment)) % 4
    padded_segment = header_segment + ("=" * padding_needed)

    try:
        decoded_bytes = base64.urlsafe_b64decode(padded_segment)
    except (binascii.Error, ValueError):
        raise ValueError("Invalid token: header is not valid base64url")

    try:
        decoded_text = decoded_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Invalid token: header is not valid UTF-8")

    try:
        header_obj = json.loads(decoded_text)
    except (json.JSONDecodeError, ValueError):
        raise ValueError("Invalid token: header is not valid JSON")

    if not isinstance(header_obj, dict):
        raise ValueError("Invalid token: header is not a JSON object")

    return header_obj
