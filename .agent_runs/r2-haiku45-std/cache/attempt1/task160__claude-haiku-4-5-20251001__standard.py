import hashlib
import hmac
from typing import Union


def pbkdf2_hash(password: str, salt: Union[bytes, bytearray], iterations: int, dklen: int = 32) -> str:
    """
    Derive a key from password using PBKDF2-HMAC-SHA256.
    
    Args:
        password: The password as a string (will be UTF-8 encoded)
        salt: The salt as bytes or bytearray
        iterations: Number of iterations (must be >= 1)
        dklen: Derived key length in bytes (default 32, must be >= 1)
    
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
    if isinstance(iterations, bool) or not isinstance(iterations, int):
        raise TypeError("iterations must be an int")
    if isinstance(dklen, bool) or not isinstance(dklen, int):
        raise TypeError("dklen must be an int")
    
    # Value validation
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    if dklen < 1:
        raise ValueError("dklen must be >= 1")
    
    # Derive key using PBKDF2-HMAC-SHA256
    derived_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        bytes(salt),
        iterations,
        dklen=dklen
    )
    
    return derived_key.hex()


def verify_password(password: str, salt: Union[bytes, bytearray], iterations: int, expected_hex: str) -> bool:
    """
    Verify a password by re-deriving the key and comparing with expected_hex.
    
    Uses constant-time comparison (hmac.compare_digest) to prevent timing attacks.
    
    Args:
        password: The password to verify
        salt: The salt used in the original derivation
        iterations: Number of iterations used in the original derivation
        expected_hex: The expected derived key as a hex string
    
    Returns:
        True if the re-derived key matches expected_hex, False otherwise
    
    Raises:
        TypeError: If password is not str, salt is not bytes/bytearray, 
                   or iterations is not int (bool excluded)
        ValueError: If expected_hex is not valid hex of even length
    """
    # Validate expected_hex format
    if not isinstance(expected_hex, str):
        raise ValueError("expected_hex must be a string")
    
    if len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must have even length")
    
    try:
        # Try to decode as hex to validate it's valid hex
        bytes.fromhex(expected_hex)
    except ValueError:
        raise ValueError("expected_hex must be valid hex")
    
    # Infer dklen from expected_hex length
    dklen = len(expected_hex) // 2
    
    # Re-derive the key (this will also validate password, salt, iterations types)
    derived_hex = pbkdf2_hash(password, salt, iterations, dklen)
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(derived_hex.lower(), expected_hex.lower())
