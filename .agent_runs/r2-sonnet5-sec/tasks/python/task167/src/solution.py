"""RFC 7617 HTTP Basic authentication header encode/decode utilities.

Implements:
    encode_basic_auth(username: str, password: str) -> str
    decode_basic_auth(header: str) -> tuple[str, str]

Only the Python standard library is used. Inputs are strictly validated
and no sensitive internal details are leaked via exception messages.
"""

from __future__ import annotations

import base64
import binascii

__all__ = ["encode_basic_auth", "decode_basic_auth"]


def encode_basic_auth(username: str, password: str) -> str:
    """Build a Basic auth Authorization header value.

    Raises:
        ValueError: if inputs are invalid (wrong type, or username
            contains a ':' character).
    """
    if not isinstance(username, str) or not isinstance(password, str):
        raise ValueError("username and password must be strings")

    if ":" in username:
        raise ValueError("username must not contain ':'")

    credentials = f"{username}:{password}"
    try:
        encoded_bytes = credentials.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("credentials could not be encoded as UTF-8") from exc

    token = base64.b64encode(encoded_bytes).decode("ascii")
    return f"Basic {token}"


def decode_basic_auth(header: str) -> tuple[str, str]:
    """Parse a Basic auth Authorization header value.

    Raises:
        ValueError: if the header is malformed, the scheme is not
            'basic' (case-insensitive), the token is missing/empty,
            the base64 is invalid, the decoded bytes are not valid
            UTF-8, or the decoded text has no ':' separator.
    """
    if not isinstance(header, str):
        raise ValueError("header must be a string")

    parts = header.split(" ")
    if len(parts) != 2:
        raise ValueError("malformed Authorization header")

    scheme, token = parts

    if scheme.lower() != "basic":
        raise ValueError("unsupported authentication scheme")

    if not token:
        raise ValueError("missing credentials token")

    try:
        decoded_bytes = base64.b64decode(token, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("invalid base64 token") from exc

    try:
        decoded_text = decoded_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("credentials are not valid UTF-8") from exc

    username, sep, password = decoded_text.partition(":")
    if sep == "":
        raise ValueError("credentials missing ':' separator")

    return (username, password)
