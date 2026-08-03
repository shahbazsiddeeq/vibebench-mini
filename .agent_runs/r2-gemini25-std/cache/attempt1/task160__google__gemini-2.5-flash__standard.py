import hashlib
import hmac

def _validate_inputs(password, salt, iterations, dklen=None):
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int) or isinstance(iterations, bool):
        raise TypeError("iterations must be an integer")
    if iterations < 1:
        raise ValueError("iterations must be greater than or equal to 1")
    if dklen is not None:
        if not isinstance(dklen, int) or isinstance(dklen, bool):
            raise TypeError("dklen must be an integer")
        if dklen < 1:
            raise ValueError("dklen must be greater than or equal to 1")

def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    _validate_inputs(password, salt, iterations, dklen)

    derived_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=dklen
    )
    return derived_key.hex()

def verify_password(password: str, salt: bytes, iterations: int, expected_hex: str) -> bool:
    _validate_inputs(password, salt, iterations)

    if not isinstance(expected_hex, str):
        raise TypeError("expected_hex must be a string")
    if not all(c in "0123456789abcdefABCDEF" for c in expected_hex):
        raise ValueError("expected_hex contains non-hexadecimal characters")
    if len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must have an even length")

    dklen = len(expected_hex) // 2
    
    derived_key_hex = pbkdf2_hash(password, salt, iterations, dklen)
    
    # hmac.compare_digest expects bytes, so convert hex strings to bytes
    return hmac.compare_digest(derived_key_hex.encode('ascii'), expected_hex.lower().encode('ascii'))
