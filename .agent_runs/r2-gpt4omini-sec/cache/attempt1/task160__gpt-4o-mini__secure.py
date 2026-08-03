import hashlib
import hmac
import binascii

def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int) or not isinstance(dklen, int):
        raise TypeError("iterations and dklen must be integers")
    if iterations < 1:
        raise ValueError("iterations must be at least 1")
    if dklen < 1:
        raise ValueError("dklen must be at least 1")

    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Derive the key using PBKDF2-HMAC-SHA256
    dk = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen)
    
    # Return the derived key as a lowercase hex string
    return dk.hex()

def verify_password(password: str, salt: bytes, iterations: int, expected_hex: str) -> bool:
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int):
        raise TypeError("iterations must be an integer")
    
    # Validate expected_hex
    if not isinstance(expected_hex, str) or len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must be a valid hex string of even length")
    
    try:
        # Convert expected_hex to bytes
        expected_bytes = binascii.unhexlify(expected_hex)
    except (binascii.Error, ValueError):
        raise ValueError("expected_hex must be a valid hex string")

    # Derive dklen from expected_hex
    dklen = len(expected_bytes)

    # Derive the key using PBKDF2-HMAC-SHA256
    derived_key = pbkdf2_hash(password, salt, iterations, dklen)

    # Use constant-time comparison to verify the derived key
    return hmac.compare_digest(derived_key, expected_hex)
