import hashlib
import hmac


def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    """
    Derive a key from password using PBKDF2-HMAC-SHA256.
    
    Args:
        password: Password string (UTF-8 encoded)
        salt: Salt bytes
        iterations: Number of iterations (rounds)
        dklen: Derived key length in bytes (default 32)
    
    Returns:
        Lowercase hex string of length 2*dklen
    
    Raises:
        TypeError: If types are incorrect
        ValueError: If iterations < 1 or dklen < 1
    """
    # Type validation - bool is not considered int
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
    Verify a password against an expected hash.
    
    Args:
        password: Password string to verify
        salt: Salt bytes used in original hash
        iterations: Number of iterations used in original hash
        expected_hex: Expected hash as hex string
    
    Returns:
        True if password matches, False otherwise
    
    Raises:
        TypeError: If types are incorrect
        ValueError: If expected_hex is not valid hex of even length
    """
    # Type validation for password, salt, iterations
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if type(iterations) is bool or not isinstance(iterations, int):
        raise TypeError("iterations must be an int")
    
    # Value validation for iterations
    if iterations < 1:
        raise ValueError("iterations must be >= 1")
    
    # Validate expected_hex
    if not isinstance(expected_hex, str):
        raise ValueError("expected_hex must be a string")
    
    # Check if even length
    if len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must have even length")
    
    # Check if valid hex
    try:
        bytes.fromhex(expected_hex)
    except ValueError:
        raise ValueError("expected_hex must be valid hexadecimal")
    
    # Infer dklen from expected_hex length
    dklen = len(expected_hex) // 2
    
    if dklen < 1:
        raise ValueError("dklen must be >= 1")
    
    # Derive key with inferred dklen
    derived_hex = pbkdf2_hash(password, salt, iterations, dklen)
    
    # Constant-time comparison (case-insensitive)
    return hmac.compare_digest(derived_hex.lower(), expected_hex.lower())
