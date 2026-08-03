import hashlib
import hmac
import binascii

def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int) or not isinstance(dklen, int):
        raise TypeError("iterations and dklen must be integers")
    if iterations < 1:
        raise ValueError("iterations must be at least 1")
    if dklen < 1:
        raise ValueError("dklen must be at least 1")

    password_bytes = password.encode('utf-8')
    dk = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen)
    return dk.hex()

def verify_password(password: str, salt: bytes, iterations: int, expected_hex: str) -> bool:
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int):
        raise TypeError("iterations must be an integer")
    
    if len(expected_hex) % 2 != 0 or any(c not in "0123456789abcdefABCDEF" for c in expected_hex):
        raise ValueError("expected_hex must be valid hex of even length")

    dklen = len(expected_hex) // 2
    derived_key = pbkdf2_hash(password, salt, iterations, dklen)
    return hmac.compare_digest(derived_key, expected_hex.lower())
