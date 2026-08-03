from __future__ import annotations

import hashlib
import hmac


def sign(key: bytes, message: bytes) -> str:
    if not key:
        raise ValueError("key must not be empty")
    if not message:
        raise ValueError("message must not be empty")
    return hmac.new(key, message, hashlib.sha256).hexdigest()
