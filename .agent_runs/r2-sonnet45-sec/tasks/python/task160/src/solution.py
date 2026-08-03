import hashlib
import hmac
from typing import Union


def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    """
    Derives a key from password using PBKDF2-HMAC-SHA256.
    
    Args:
        password: The password string (will be UTF-8 encoded)
        salt: The salt as bytes
        iterations: Number of iterations (must be >= 1)
        dklen: Derived key length in bytes (must be >= 1)
    
    Returns:
        Lowercase hex string of the derived key (length 2*dklen)
    
    Raises:
        TypeError: If arguments have wrong types
        ValueError: If iterations < 1 or dklen < 1
    """
    # Type validation - be strict about bool not being int
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if type(iterations) is bool or not isinstance(iterations, int):
        raise TypeError("iterations must be an int")
    if type(dklen) is bool or not isinstance(dklen, int):
        raise TypeError("dklen must be an int")
    
    # Value validation
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    if dklen < 1:
        raise ValueError("dklen must be >= 1")
    
    # Derive key using PBKDF2-HMAC-SHA256
    password_bytes = password.encode('utf-8')
    derived_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen)
    
    # Return as lowercase hex string
    return derived_key.hex()


def verify_password(password: str, salt: bytes, iterations: int, expected_hex: str) -> bool:
    """
    Verifies a password against an expected PBKDF2 hash.
    
    Args:
        password: The password to verify
        salt: The salt used in hashing
        iterations: Number of iterations used
        expected_hex: Expected hash as hex string (case-insensitive)
    
    Returns:
        True if password matches, False otherwise
    
    Raises:
        TypeError: If arguments have wrong types
        ValueError: If expected_hex is not valid hex or has odd length
    """
    # Type validation
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if type(iterations) is bool or not isinstance(iterations, int):
        raise TypeError("iterations must be an int")
    if not isinstance(expected_hex, str):
        raise TypeError("expected_hex must be a str")
    
    # Value validation for iterations
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    
    # Validate expected_hex is valid hex with even length
    if len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must have even length")
    
    try:
        # Try to decode hex to validate it's valid hex
        expected_bytes = bytes.fromhex(expected_hex)
    except ValueError:
        raise ValueError("expected_hex must be valid hexadecimal")
    
    # Infer dklen from expected_hex length
    dklen = len(expected_hex) // 2
    
    # Derive key from password
    derived_hex = pbkdf2_hash(password, salt, iterations, dklen)
    
    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(derived_hex, expected_hex.lower())
