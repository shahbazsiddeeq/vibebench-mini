import hmac
import hashlib
import struct

def totp(secret: bytes, timestamp: int, period: int = 30, digits: int = 6, algorithm: str = "sha1", t0: int = 0) -> str:
    # Validate types
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

    # Validate values
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

    # Pack counter as an 8-byte big-endian unsigned integer
    counter_bytes = struct.pack(">Q", counter)

    # Select the hash function
    hash_function = getattr(hashlib, algorithm)

    # Compute HMAC
    hmac_digest = hmac.new(secret, counter_bytes, hash_function).digest()

    # Dynamic truncation
    offset = hmac_digest[-1] & 0x0F
    truncated_hash = hmac_digest[offset:offset + 4]

    # Convert to a 31-bit integer
    code = struct.unpack(">I", truncated_hash)[0] & 0x7FFFFFFF

    # Modulo to get the final code
    code %= 10 ** digits

    # Return zero-padded code
    return str(code).zfill(digits)
