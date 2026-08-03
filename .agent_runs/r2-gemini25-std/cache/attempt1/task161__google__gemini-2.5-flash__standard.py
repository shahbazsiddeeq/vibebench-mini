import hmac
import hashlib
import struct

def totp(secret: bytes, timestamp: int, period: int = 30,
         digits: int = 6, algorithm: str = "sha1", t0: int = 0) -> str:
    """
    Computes a Time-based One-Time Password per RFC 6238 / RFC 4226.

    Args:
        secret: The shared secret key as bytes.
        timestamp: The current Unix timestamp (seconds since epoch).
        period: The time step in seconds (default: 30).
        digits: The number of digits in the OTP (default: 6).
        algorithm: The HMAC hash algorithm ("sha1", "sha256", or "sha512") (default: "sha1").
        t0: The Unix time to start counting time steps (default: 0).

    Returns:
        The TOTP as a zero-padded decimal string.

    Raises:
        TypeError: If secret is not bytes/bytearray, or if timestamp, period, digits, t0
                   are not integers (bool is not accepted).
        ValueError: If period < 1, digits not in 1..10, algorithm is invalid, or timestamp < t0.
    """

    # Type validation
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")
    for arg_name, arg_value in [("timestamp", timestamp), ("period", period), ("digits", digits), ("t0", t0)]:
        if not isinstance(arg_value, int) or isinstance(arg_value, bool):
            raise TypeError(f"{arg_name} must be an int")

    # Value validation
    if period < 1:
        raise ValueError("period must be at least 1")
    if not (1 <= digits <= 10):
        raise ValueError("digits must be between 1 and 10 inclusive")
    if algorithm not in ["sha1", "sha256", "sha512"]:
        raise ValueError("algorithm must be 'sha1', 'sha256', or 'sha512'")
    if timestamp < t0:
        raise ValueError("timestamp cannot be less than t0")

    # Calculate counter
    counter = (timestamp - t0) // period

    # Pack counter as an 8-byte big-endian unsigned integer
    # 'Q' for unsigned long long (8 bytes), network byte order (big-endian)
    packed_counter = struct.pack(">Q", counter)

    # Compute HMAC
    if algorithm == "sha1":
        hash_func = hashlib.sha1
    elif algorithm == "sha256":
        hash_func = hashlib.sha256
    else: # algorithm == "sha512"
        hash_func = hashlib.sha512

    hmac_result = hmac.new(secret, packed_counter, hash_func).digest()

    # Apply dynamic truncation
    offset = hmac_result[-1] & 0x0F
    truncated_hash = hmac_result[offset : offset + 4]

    # Convert to 31-bit integer
    # '>I' for unsigned int (4 bytes), network byte order (big-endian)
    # Mask off the top bit (0x7FFFFFFF) to get a 31-bit integer
    otp_value = struct.unpack(">I", truncated_hash)[0] & 0x7FFFFFFF

    # Take modulo 10**digits
    mod_divisor = 10**digits
    otp_code = otp_value % mod_divisor

    # Return as zero-padded decimal string
    return str(otp_code).zfill(digits)
