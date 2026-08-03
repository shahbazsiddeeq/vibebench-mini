"""Utilities for encoding and decoding HTTP Basic authentication values."""

from __future__ import annotations

import base64
import binascii


def encode_basic_auth(username: str, password: str) -> str:
    """Return an RFC 7617 Basic Authorization header value."""
    if not isinstance(username, str) or not isinstance(password, str):
        raise ValueError("username and password must be strings")
    if ":" in username:
        raise ValueError("username must not contain ':'")

    try:
        credentials = f"{username}:{password}".encode("utf-8")
    except UnicodeEncodeError:
        raise ValueError("credentials must be valid Unicode") from None

    token = base64.b64encode(credentials).decode("ascii")
    return "Basic " + token


def decode_basic_auth(header: str) -> tuple[str, str]:
    """Decode an RFC 7617 Basic Authorization header value."""
    if not isinstance(header, str):
        raise ValueError("header must be a string")

    if len(header) <= 6 or header[:5].lower() != "basic" or header[5] != " ":
        raise ValueError("invalid Basic authentication header")

    token = header[6:]
    if not token:
        raise ValueError("missing Basic authentication token")

    try:
        decoded = base64.b64decode(token, validate=True)
    except (binascii.Error, ValueError, UnicodeEncodeError):
        raise ValueError("invalid base64 token") from None

    # Require canonical standard Base64, including correct '=' padding.
    if base64.b64encode(decoded).decode("ascii") != token:
        raise ValueError("invalid base64 token")

    try:
        credentials = decoded.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("credentials are not valid UTF-8") from None

    if ":" not in credentials:
        raise ValueError("decoded credentials contain no separator")

    username, password = credentials.split(":", 1)
    return username, password
