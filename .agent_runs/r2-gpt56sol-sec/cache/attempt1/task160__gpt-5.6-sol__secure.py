"""PBKDF2-HMAC-SHA256 password key derivation and verification."""

import hashlib
import hmac


def _validate_inputs(
    password: str, salt: bytes | bytearray, iterations: int
) -> None:
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if isinstance(iterations, bool) or not isinstance(iterations, int):
        raise TypeError("iterations must be an int")
    if iterations < 1:
        raise ValueError("iterations must be at least 1")


def pbkdf2_hash(
    password: str,
    salt: bytes | bytearray,
    iterations: int,
    dklen: int = 32,
) -> str:
    """Derive a lowercase hexadecimal key using PBKDF2-HMAC-SHA256."""
    _validate_inputs(password, salt, iterations)

    if isinstance(dklen, bool) or not isinstance(dklen, int):
        raise TypeError("dklen must be an int")
    if dklen < 1:
        raise ValueError("dklen must be at least 1")

    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes(salt),
        iterations,
        dklen=dklen,
    )
    return derived_key.hex()


def verify_password(
    password: str,
    salt: bytes | bytearray,
    iterations: int,
    expected_hex: str,
) -> bool:
    """Verify a password against a hexadecimal PBKDF2-derived key."""
    _validate_inputs(password, salt, iterations)

    if not isinstance(expected_hex, str):
        raise ValueError("expected_hex must be a valid even-length hexadecimal string")
    if not expected_hex or len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must be a valid even-length hexadecimal string")

    try:
        expected_key = bytes.fromhex(expected_hex)
    except ValueError:
        raise ValueError(
            "expected_hex must be a valid even-length hexadecimal string"
        ) from None

    # bytes.fromhex accepts whitespace, so reject inputs whose decoded size does
    # not correspond exactly to the original string length.
    if len(expected_key) * 2 != len(expected_hex):
        raise ValueError("expected_hex must be a valid even-length hexadecimal string")

    actual_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes(salt),
        iterations,
        dklen=len(expected_key),
    )
    return hmac.compare_digest(actual_key, expected_key)
