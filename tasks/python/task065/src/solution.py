from __future__ import annotations

import base64
import binascii


def b64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64_decode(s: str) -> bytes:
    try:
        return base64.b64decode(s, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"invalid base64: {exc}") from exc
