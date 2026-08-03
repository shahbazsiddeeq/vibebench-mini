import hashlib
import hmac


def _check_common(password, salt, iterations):
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if isinstance(iterations, bool) or not isinstance(iterations, int):
        raise TypeError("iterations must be an int")
    if iterations < 1:
        raise ValueError("iterations must be >= 1")


def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    _check_common(password, salt, iterations)
    if isinstance(dklen, bool) or not isinstance(dklen, int):
        raise TypeError("dklen must be an int")
    if dklen < 1:
        raise ValueError("dklen must be >= 1")

    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes(salt),
        iterations,
        dklen=dklen,
    )
    return dk.hex()


def verify_password(password: str, salt: bytes, iterations: int, expected_hex: str) -> bool:
    _check_common(password, salt, iterations)
    if not isinstance(expected_hex, str):
        raise TypeError("expected_hex must be a str")

    if len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must have even length")
    try:
        expected_bytes = bytes.fromhex(expected_hex)
    except ValueError:
        raise ValueError("expected_hex must be valid hex")

    dklen = len(expected_hex) // 2
    if dklen < 1:
        raise ValueError("dklen must be >= 1")

    derived_hex = pbkdf2_hash(password, salt, iterations, dklen)
    derived_bytes = bytes.fromhex(derived_hex)

    return hmac.compare_digest(derived_bytes, expected_bytes)
