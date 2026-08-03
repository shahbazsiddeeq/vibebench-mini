import hmac
import hashlib
import struct

def totp(secret: bytes, timestamp: int, period: int = 30,
         digits: int = 6, algorithm: str = "sha1", t0: int = 0) -> str:
    """
    Computes a Time-based One-Time Password (TOTP) per RFC 6238 / RFC 4226.

    Args:
        secret: The shared secret key as bytes.
        timestamp: The current Unix timestamp (seconds since epoch).
        period: The time step in seconds (default 30).
        digits: The number of digits in the TOTP code (1-10, default 6).
        algorithm: The HMAC hash algorithm ("sha1", "sha256", or "sha512", default "sha1").
        t0: The Unix time to start counting time steps (default 0).

    Returns:
        The TOTP code as a zero-padded decimal string.

    Raises:
        TypeError: If secret is not bytes/bytearray, or if timestamp, period, digits,
                   or t0 are not integers (bool is not accepted as an int).
        ValueError: If period < 1, digits is not in 1..10, algorithm is invalid,
                    or timestamp < t0.
    """

    # Input validation
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")
    if not isinstance(timestamp, int) or isinstance(timestamp, bool):
        raise TypeError("timestamp must be an integer")
    if not isinstance(period, int) or isinstance(period, bool):
        raise TypeError("period must be an integer")
    if not isinstance(digits, int) or isinstance(digits, bool):
        raise TypeError("digits must be an integer")
    if not isinstance(t0, int) or isinstance(t0, bool):
        raise TypeError("t0 must be an integer")

    if period < 1:
        raise ValueError("period must be at least 1")
    if not (1 <= digits <= 10):
        raise ValueError("digits must be between 1 and 10 inclusive")
    if timestamp < t0:
        raise ValueError("timestamp cannot be less than t0")

    hash_algorithms = {
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    if algorithm not in hash_algorithms:
        raise ValueError(f"algorithm must be one of {list(hash_algorithms.keys())}")

    # Calculate counter
    counter = (timestamp - t0) // period

    # Pack counter as an 8-byte big-endian unsigned integer
    # '!' for network byte order (big-endian), 'Q' for unsigned long long (8 bytes)
    message = struct.pack("!Q", counter)

    # Compute HMAC
    hmac_hasher = hmac.new(secret, message, hash_algorithms[algorithm])
    hmac_digest = hmac_hasher.digest()

    # Apply dynamic truncation (RFC 4226, Section 5.4)
    offset = hmac_digest[-1] & 0x0F
    truncated_hash = hmac_digest[offset : offset + 4]

    # Convert to 31-bit integer
    # '!' for network byte order (big-endian), 'I' for unsigned int (4 bytes)
    # Mask off the top bit to get a 31-bit integer
    otp_value = struct.unpack("!I", truncated_hash)[0] & 0x7FFFFFFF

    # Take modulo 10**digits
    mod_value = 10 ** digits
    totp_code = otp_value % mod_value

    # Return as a decimal string zero-padded to exactly `digits` characters
    return str(totp_code).zfill(digits)
