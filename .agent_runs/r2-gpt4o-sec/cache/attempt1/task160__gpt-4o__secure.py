import hashlib
import hmac

def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int) or isinstance(iterations, bool):
        raise TypeError("iterations must be an int")
    if not isinstance(dklen, int) or isinstance(dklen, bool):
        raise TypeError("dklen must be an int")
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    if dklen < 1:
        raise ValueError("dklen must be >= 1")

    derived_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen
    )
    return derived_key.hex()

def verify_password(password: str, salt: bytes, iterations: int, expected_hex: str) -> bool:
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int) or isinstance(iterations, bool):
        raise TypeError("iterations must be an int")
    if not isinstance(expected_hex, str):
        raise TypeError("expected_hex must be a str")
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    if len(expected_hex) % 2 != 0 or not all(c in "0123456789abcdefABCDEF" for c in expected_hex):
        raise ValueError("expected_hex must be valid hex of even length")

    dklen = len(expected_hex) // 2
    derived_key = pbkdf2_hash(password, salt, iterations, dklen)
    return hmac.compare_digest(derived_key, expected_hex.lower())
