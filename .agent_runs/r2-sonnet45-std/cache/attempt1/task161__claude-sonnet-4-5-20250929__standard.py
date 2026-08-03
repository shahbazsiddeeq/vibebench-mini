import hmac
import hashlib
import struct


def totp(secret: bytes, timestamp: int, period: int = 30,
         digits: int = 6, algorithm: str = "sha1", t0: int = 0) -> str:
    """
    Compute a Time-based One-Time Password per RFC 6238 / RFC 4226.
    
    Args:
        secret: The shared secret key (bytes)
        timestamp: Current Unix timestamp
        period: Time step in seconds (default 30)
        digits: Number of digits in the output (1-10, default 6)
        algorithm: Hash algorithm ("sha1", "sha256", or "sha512")
        t0: Unix time to start counting time steps (default 0)
    
    Returns:
        TOTP code as a zero-padded decimal string
    """
    # Type validation
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")
    
    # Check that timestamp, period, digits, t0 are int (not bool)
    if isinstance(timestamp, bool) or not isinstance(timestamp, int):
        raise TypeError("timestamp must be an int")
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int")
    if isinstance(digits, bool) or not isinstance(digits, int):
        raise TypeError("digits must be an int")
    if isinstance(t0, bool) or not isinstance(t0, int):
        raise TypeError("t0 must be an int")
    
    # Value validation
    if period < 1:
        raise ValueError("period must be >= 1")
    if not (1 <= digits <= 10):
        raise ValueError("digits must be between 1 and 10 inclusive")
    if algorithm not in ("sha1", "sha256", "sha512"):
        raise ValueError("algorithm must be 'sha1', 'sha256', or 'sha512'")
    if timestamp < t0:
        raise ValueError("timestamp must be >= t0")
    
    # Calculate counter
    counter = (timestamp - t0) // period
    
    # Pack counter as 8-byte big-endian unsigned integer
    counter_bytes = struct.pack(">Q", counter)
    
    # Get hash function
    hash_func = getattr(hashlib, algorithm)
    
    # Compute HMAC
    hmac_result = hmac.new(secret, counter_bytes, hash_func).digest()
    
    # Dynamic truncation
    # Use low 4 bits of last byte as offset
    offset = hmac_result[-1] & 0x0F
    
    # Extract 4 bytes starting at offset
    truncated = struct.unpack(">I", hmac_result[offset:offset+4])[0]
    
    # Mask off the top bit (to get 31-bit integer)
    truncated &= 0x7FFFFFFF
    
    # Take modulo 10^digits
    code = truncated % (10 ** digits)
    
    # Return as zero-padded string
    return str(code).zfill(digits)
