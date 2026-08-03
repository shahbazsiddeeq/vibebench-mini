from __future__ import annotations

import base64
import json


def decode_jwt_header(token: str) -> dict:
    if "." not in token:
        raise ValueError("not a valid JWT: no '.' separator")
    header_b64 = token.split(".")[0]
    # Add padding
    padding = 4 - len(header_b64) % 4
    if padding != 4:
        header_b64 += "=" * padding
    try:
        decoded = base64.urlsafe_b64decode(header_b64)
    except Exception as exc:
        raise ValueError(f"invalid base64: {exc}") from exc
    try:
        header = json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise ValueError(f"header is not valid JSON: {exc}") from exc
    if not isinstance(header, dict):
        raise ValueError("JWT header must be a JSON object")
    return header
