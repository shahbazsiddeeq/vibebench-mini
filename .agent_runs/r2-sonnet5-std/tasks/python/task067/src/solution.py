import secrets
import base64


def gen_token(n_bytes: int = 32) -> str:
    if n_bytes < 8:
        raise ValueError("n_bytes must be >= 8")
    raw = secrets.token_bytes(n_bytes)
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii')
