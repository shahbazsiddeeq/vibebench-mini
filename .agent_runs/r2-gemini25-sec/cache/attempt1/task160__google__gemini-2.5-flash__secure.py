import hashlib
import hmac
import secrets

def _validate_pbkdf2_inputs(password, salt, iterations, dklen):
    """
    Internal helper to validate common inputs for pbkdf2_hash and verify_password.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int) or isinstance(iterations, bool):
        raise TypeError("iterations must be an integer")
    if not isinstance(dklen, int) or isinstance(dklen, bool):
        raise TypeError("dklen must be an integer")

    if iterations < 1:
        raise ValueError("iterations must be at least 1")
    if dklen < 1:
        raise ValueError("dklen must be at least 1")

def pbkdf2_hash(password: str, salt: bytes, iterations: int, dklen: int = 32) -> str:
    """
    Derives a key from the UTF-8 encoding of `password` using PBKDF2-HMAC-SHA256.

    Args:
        password: The password string.
        salt: The salt bytes.
        iterations: The number of PBKDF2 iterations (rounds).
        dklen: The desired length of the derived key in bytes.

    Returns:
        The derived key as a lowercase hex string.

    Raises:
        TypeError: If input types are incorrect.
        ValueError: If iterations or dklen are less than 1.
    """
    _validate_pbkdf2_inputs(password, salt, iterations, dklen)

    derived_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=dklen
    )
    return derived_key.hex()

def verify_password(password: str, salt: bytes, iterations: int, expected_hex: str) -> bool:
    """
    Re-derives the key and compares it to an expected hex string using a constant-time
    comparison.

    Args:
        password: The password string.
        salt: The salt bytes.
        iterations: The number of PBKDF2 iterations (rounds).
        expected_hex: The expected derived key as a lowercase hex string.

    Returns:
        True if the re-derived key matches `expected_hex`, False otherwise.

    Raises:
        TypeError: If input types are incorrect.
        ValueError: If iterations is less than 1 or expected_hex is not valid hex
                    or has an odd length.
    """
    # Validate password, salt, iterations first, dklen will be inferred.
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes or bytearray")
    if not isinstance(iterations, int) or isinstance(iterations, bool):
        raise TypeError("iterations must be an integer")
    if iterations < 1:
        raise ValueError("iterations must be at least 1")

    if not isinstance(expected_hex, str):
        raise TypeError("expected_hex must be a string")

    # Validate expected_hex format
    if len(expected_hex) % 2 != 0:
        raise ValueError("expected_hex must have an even length")
    try:
        expected_bytes = bytes.fromhex(expected_hex)
    except ValueError as e:
        raise ValueError(f"expected_hex is not valid hexadecimal: {e}")

    dklen = len(expected_bytes)
    # dklen is derived from expected_hex, so it's guaranteed to be >= 1 if expected_hex is valid.
    # No need to check dklen < 1 explicitly here, as len(expected_bytes) will be >= 1.

    # Re-derive the key
    derived_key_bytes = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=dklen
    )

    # Constant-time comparison
    return hmac.compare_digest(derived_key_bytes, expected_bytes)
