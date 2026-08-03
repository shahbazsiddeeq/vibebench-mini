"""
PBKDF2-HMAC-SHA256 password key derivation and verification utilities.

Uses only the Python standard library (hashlib, hmac).
"""

import hashlib
import hmac


def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    """
    Derive a key from `password` using PBKDF2-HMAC-SHA256.

    Returns the derived key as a lowercase hex string of length 2*dklen.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if isinstance(iterations, bool) or not isinstance(iterations, int):
        raise TypeError("iterations must be an int")
    if isinstance(dklen, bool) or not isinstance(dklen, int):
        raise TypeError("dklen must be an int")
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    if dklen < 1:
        raise ValueError("dklen must be >= 1")

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes(salt),
        iterations,
        dklen=dklen,
    )
    return derived.hex()


def verify_password(
    password: str, salt: bytes, iterations: int, expected_hex: str
) -> bool:
    """
    Re-derive the key for `password` and compare it against `expected_hex`
    using a constant-time comparison.

    dklen is inferred as len(expected_hex) // 2.
    """
    if not isinstance(expected_hex, str):
        raise TypeError("expected_hex must be a str")
    if len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must have even length")
    try:
        expected_bytes = bytes.fromhex(expected_hex)
    except ValueError:
        raise ValueError("expected_hex must be a valid hex string")

    dklen = len(expected_hex) // 2
    if dklen < 1:
        raise ValueError("dklen must be >= 1")

    computed_hex = pbkdf2_hash(password, salt, iterations, dklen)
    computed_bytes = bytes.fromhex(computed_hex)

    return hmac.compare_digest(computed_bytes, expected_bytes)
