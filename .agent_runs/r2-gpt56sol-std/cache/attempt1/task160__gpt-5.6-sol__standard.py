import hashlib
import hmac


def _validate_inputs(
    password: str, salt: bytes | bytearray, iterations: int, dklen: int
) -> None:
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int) or isinstance(iterations, bool):
        raise TypeError("iterations must be an int")
    if not isinstance(dklen, int) or isinstance(dklen, bool):
        raise TypeError("dklen must be an int")
    if iterations < 1:
        raise ValueError("iterations must be at least 1")
    if dklen < 1:
        raise ValueError("dklen must be at least 1")


def pbkdf2_hash(
    password: str, salt: bytes, iterations: int, dklen: int = 32
) -> str:
    """Derive a key using PBKDF2-HMAC-SHA256 and return lowercase hexadecimal."""
    _validate_inputs(password, salt, iterations, dklen)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes(salt),
        iterations,
        dklen=dklen,
    )
    return derived_key.hex()


def verify_password(
    password: str, salt: bytes, iterations: int, expected_hex: str
) -> bool:
    """Verify a password against a hexadecimal PBKDF2-HMAC-SHA256 key."""
    if not isinstance(expected_hex, str):
        raise ValueError("expected_hex must be a valid even-length hexadecimal string")
    if (
        not expected_hex
        or len(expected_hex) % 2 != 0
        or any(character not in "0123456789abcdefABCDEF" for character in expected_hex)
    ):
        raise ValueError("expected_hex must be a valid even-length hexadecimal string")

    expected_key = bytes.fromhex(expected_hex)
    dklen = len(expected_key)
    _validate_inputs(password, salt, iterations, dklen)

    actual_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes(salt),
        iterations,
        dklen=dklen,
    )
    return hmac.compare_digest(actual_key, expected_key)
