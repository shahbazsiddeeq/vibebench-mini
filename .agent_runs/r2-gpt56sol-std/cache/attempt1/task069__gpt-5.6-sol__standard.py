import base64
import binascii
import json
import re
from typing import Any


_BASE64URL_RE = re.compile(r"^[A-Za-z0-9_-]*={0,2}$")


def decode_jwt_header(token: str) -> dict[str, Any]:
    """Decode and return a JWT header without validating its signature."""
    if not isinstance(token, str) or "." not in token:
        raise ValueError("token must contain a '.' separator")

    segment = token.split(".", 1)[0]

    if not _BASE64URL_RE.fullmatch(segment):
        raise ValueError("invalid base64url header")

    unpadded = segment.rstrip("=")
    supplied_padding = len(segment) - len(unpadded)
    remainder = len(unpadded) % 4

    if remainder == 1:
        raise ValueError("invalid base64url header")

    required_padding = (4 - remainder) % 4
    if supplied_padding and supplied_padding != required_padding:
        raise ValueError("invalid base64url padding")

    padded = unpadded + ("=" * required_padding)

    try:
        decoded = base64.b64decode(
            padded.encode("ascii"),
            altchars=b"-_",
            validate=True,
        )
    except (UnicodeEncodeError, binascii.Error, ValueError) as exc:
        raise ValueError("invalid base64url header") from exc

    canonical = base64.urlsafe_b64encode(decoded).decode("ascii").rstrip("=")
    if canonical != unpadded:
        raise ValueError("invalid base64url header")

    def reject_constant(value: str) -> Any:
        raise ValueError(f"invalid JSON constant: {value}")

    try:
        header = json.loads(
            decoded.decode("utf-8"),
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError("JWT header is not valid JSON") from exc

    if not isinstance(header, dict):
        raise ValueError("JWT header JSON must be an object")

    return header
