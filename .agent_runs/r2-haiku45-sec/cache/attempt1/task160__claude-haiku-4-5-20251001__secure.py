import hashlib
import hmac
from typing import Union


def pbkdf2_hash(password: str, salt: Union[bytes, bytearray], iterations: int, dklen: int = 32) -> str:
    """
    Derive a key from a password using PBKDF2-HMAC-SHA256.
    
    Args:
        password: The password as a string (will be UTF-8 encoded)
        salt: The salt as bytes or bytearray
        iterations: Number of iterations (must be >= 1)
        dklen: Derived key length in bytes (must be >= 1, default 32)
    
    Returns:
        The derived key as a lowercase hex string of length 2*dklen
    
    Raises:
        TypeError: If password is not str, salt is not bytes/bytearray, 
                   or iterations/dklen is not int (bool excluded)
        ValueError: If iterations < 1 or dklen < 1
    """
    # Type validation
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    
    # Explicitly reject bool (which is a subclass of int in Python)
    if isinstance(iterations, bool) or not isinstance(iterations, int):
        raise TypeError("iterations must be an int")
    
    if isinstance(dklen, bool) or not isinstance(dklen, int):
        raise TypeError("dklen must be an int")
    
    # Value validation
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    
    if dklen < 1:
        raise ValueError("dklen must be >= 1")
    
    # Perform PBKDF2-HMAC-SHA256
    password_bytes = password.encode('utf-8')
    derived_key = hashlib.pbkdf2_hmac(
        'sha256',
        password_bytes,
        bytes(salt),
        iterations,
        dklen=dklen
    )
    
    return derived_key.hex()


def verify_password(password: str, salt: Union[bytes, bytearray], iterations: int, expected_hex: str) -> bool:
    """
    Verify a password against a PBKDF2-HMAC-SHA256 derived key using constant-time comparison.
    
    Args:
        password: The password to verify as a string
        salt: The salt as bytes or bytearray
        iterations: Number of iterations (must be >= 1)
        expected_hex: The expected derived key as a hex string
    
    Returns:
        True if the password matches the expected hash, False otherwise
    
    Raises:
        TypeError: If password is not str, salt is not bytes/bytearray, 
                   or iterations is not int (bool excluded)
        ValueError: If expected_hex is not valid hex of even length
    """
    # Validate expected_hex format
    if not isinstance(expected_hex, str):
        raise ValueError("expected_hex must be a string")
    
    # Check if it's valid hex and has even length
    if len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must have even length")
    
    try:
        bytes.fromhex(expected_hex)
    except ValueError:
        raise ValueError("expected_hex must be valid hexadecimal")
    
    # Infer dklen from expected_hex length
    dklen = len(expected_hex) // 2
    
    # Derive the key from the provided password
    derived_hex = pbkdf2_hash(password, salt, iterations, dklen)
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(derived_hex.lower(), expected_hex.lower())
