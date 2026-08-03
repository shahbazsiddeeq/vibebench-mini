# src/solution.py

import hmac
import hashlib
import struct

def totp(secret: bytes, timestamp: int, period: int = 30, digits: int = 6, 
         algorithm: str = "sha1", t0: int = 0) -> str:
    # Validate inputs
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")
    if not all(isinstance(arg, int) for arg in [timestamp, period, digits, t0]):
        raise TypeError("timestamp, period, digits, and t0 must be integers")
    if period < 1:
        raise ValueError("period must be at least 1")
    if not (1 <= digits <= 10):
        raise ValueError("digits must be between 1 and 10 inclusive")
    if algorithm not in {"sha1", "sha256", "sha512"}:
        raise ValueError("algorithm must be one of 'sha1', 'sha256', or 'sha512'")
    if timestamp < t0:
        raise ValueError("timestamp must be greater than or equal to t0")

    # Calculate counter
    counter = (timestamp - t0) // period

    # Pack counter as an 8-byte big-endian unsigned integer
    counter_bytes = struct.pack('>Q', counter)

    # Create HMAC
    hash_func = {
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }[algorithm]
    
    hmac_result = hmac.new(secret, counter_bytes, hash_func).digest()

    # Dynamic truncation
    offset = hmac_result[-1] & 0x0F
    truncated_hash = (hmac_result[offset] & 0x7F) << 24 | \
                     (hmac_result[offset + 1] << 16) | \
                     (hmac_result[offset + 2] << 8) | \
                     hmac_result[offset + 3]

    # Modulo and zero-padding
    otp = truncated_hash % (10 ** digits)
    return str(otp).zfill(digits)
