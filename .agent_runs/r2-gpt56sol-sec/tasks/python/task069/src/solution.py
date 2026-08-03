"""Utilities for decoding JWT headers without signature validation."""

import base64
import binascii
import json
import re
from typing import Any

_BASE64URL_RE = re.compile(r"^[A-Za-z0-9_-]+={0,2}$")


def _reject_nonstandard_json_constant(value: str) -> Any:
    """Reject NaN and Infinity, which are not valid JSON values."""
    raise ValueError("Invalid JSON constant")


def decode_jwt_header(token: str) -> dict:
    """Decode and return a JWT header without validating the signature.

    Raises:
        ValueError: If the token or encoded header is malformed, the header is
            not valid JSON, or the decoded JSON value is not an object.
    """
    if not isinstance(token, str) or "." not in token:
        raise ValueError("Invalid JWT token")

    encoded_header = token.split(".", 1)[0]
    if not encoded_header or not _BASE64URL_RE.fullmatch(encoded_header):
        raise ValueError("Invalid JWT header encoding")

    # If padding is present, it must already form a complete Base64 value.
    if "=" in encoded_header and len(encoded_header) % 4 != 0:
        raise ValueError("Invalid JWT header encoding")

    padded_header = encoded_header + ("=" * (-len(encoded_header) % 4))

    try:
        decoded = base64.b64decode(
            padded_header.encode("ascii"),
            altchars=b"-_",
            validate=True,
        )
    except (UnicodeEncodeError, binascii.Error, ValueError) as exc:
        raise ValueError("Invalid JWT header encoding") from exc

    try:
        header = json.loads(
            decoded.decode("utf-8"),
            parse_constant=_reject_nonstandard_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise ValueError("Invalid JWT header JSON") from exc

    if not isinstance(header, dict):
        raise ValueError("JWT header must be a JSON object")

    return header
