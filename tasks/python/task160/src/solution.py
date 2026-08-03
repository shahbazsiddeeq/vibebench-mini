"""PBKDF2-HMAC-SHA256 password key derivation and constant-time verification."""

import hashlib
import hmac


def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    if not isinstance(password, str):
        raise TypeError("password must be str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes")
    if isinstance(iterations, bool) or not isinstance(iterations, int):
        raise TypeError("iterations must be int")
    if isinstance(dklen, bool) or not isinstance(dklen, int):
        raise TypeError("dklen must be int")
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    if dklen < 1:
        raise ValueError("dklen must be >= 1")
    dk = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes(salt), iterations, dklen
    )
    return dk.hex()


def verify_password(
    password: str, salt: bytes, iterations: int, expected_hex: str
) -> bool:
    if not isinstance(expected_hex, str):
        raise TypeError("expected_hex must be str")
    try:
        expected = bytes.fromhex(expected_hex)
    except ValueError:
        raise ValueError("expected_hex must be valid hex of even length")
    dklen = len(expected)
    if dklen < 1:
        raise ValueError("expected_hex must decode to at least one byte")
    actual_hex = pbkdf2_hash(password, salt, iterations, dklen)
    return hmac.compare_digest(actual_hex, expected_hex.lower())
