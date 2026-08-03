from __future__ import annotations

import base64
import secrets


def gen_token(n_bytes: int = 32) -> str:
    if n_bytes < 8:
        raise ValueError("n_bytes must be at least 8")
    return (
        base64.urlsafe_b64encode(secrets.token_bytes(n_bytes))
        .rstrip(b"=")
        .decode("ascii")
    )
