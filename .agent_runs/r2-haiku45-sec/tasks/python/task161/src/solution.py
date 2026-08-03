import hmac
import hashlib
import struct
from typing import Union


def totp(
    secret: Union[bytes, bytearray],
    timestamp: int,
    period: int = 30,
    digits: int = 6,
    algorithm: str = "sha1",
    t0: int = 0,
) -> str:
    """
    Compute a Time-based One-Time Password per RFC 6238 / RFC 4226.
    
    Args:
        secret: The shared secret as bytes or bytearray
        timestamp: The current Unix timestamp
        period: The time period in seconds (default 30)
        digits: Number of digits in the output (1-10, default 6)
        algorithm: Hash algorithm ("sha1", "sha256", or "sha512")
        t0: The Unix timestamp of the initial counter (default 0)
    
    Returns:
        A zero-padded decimal string of exactly `digits` characters
    
    Raises:
        TypeError: If secret is not bytes/bytearray or if any numeric parameter is not int
        ValueError: If parameters are out of valid ranges
    """
    # Type validation
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")
    
    if not isinstance(timestamp, int) or isinstance(timestamp, bool):
        raise TypeError("timestamp must be an int")
    
    if not isinstance(period, int) or isinstance(period, bool):
        raise TypeError("period must be an int")
    
    if not isinstance(digits, int) or isinstance(digits, bool):
        raise TypeError("digits must be an int")
    
    if not isinstance(t0, int) or isinstance(t0, bool):
        raise TypeError("t0 must be an int")
    
    # Value validation
    if period < 1:
        raise ValueError("period must be >= 1")
    
    if digits < 1 or digits > 10:
        raise ValueError("digits must be between 1 and 10 inclusive")
    
    if algorithm not in ("sha1", "sha256", "sha512"):
        raise ValueError("algorithm must be one of: sha1, sha256, sha512")
    
    if timestamp < t0:
        raise ValueError("timestamp must be >= t0")
    
    # Compute counter
    counter = (timestamp - t0) // period
    
    # Pack counter as 8-byte big-endian unsigned integer
    message = struct.pack(">Q", counter)
    
    # Get the hash function
    hash_func = getattr(hashlib, algorithm)
    
    # Compute HMAC
    h = hmac.new(secret, message, hash_func)
    hmac_result = h.digest()
    
    # Dynamic truncation: use low 4 bits of last byte as offset
    offset = hmac_result[-1] & 0x0f
    
    # Extract 4 bytes starting at offset
    p = hmac_result[offset : offset + 4]
    
    # Convert to 32-bit big-endian integer
    value = struct.unpack(">I", p)[0]
    
    # Mask off the top bit to get 31-bit integer
    value = value & 0x7fffffff
    
    # Take modulo 10**digits
    code = value % (10 ** digits)
    
    # Return as zero-padded decimal string
    return str(code).zfill(digits)
