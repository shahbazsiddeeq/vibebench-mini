import hashlib
import hmac
import struct


def totp(
    secret: bytes,
    timestamp: int,
    period: int = 30,
    digits: int = 6,
    algorithm: str = "sha1",
    t0: int = 0,
) -> str:
    """Generate a Time-based One-Time Password according to RFC 6238."""
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")

    for name, value in (
        ("timestamp", timestamp),
        ("period", period),
        ("digits", digits),
        ("t0", t0),
    ):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{name} must be an int")

    if period < 1:
        raise ValueError("period must be at least 1")
    if not 1 <= digits <= 10:
        raise ValueError("digits must be between 1 and 10")
    if not isinstance(algorithm, str) or algorithm not in ("sha1", "sha256", "sha512"):
        raise ValueError("algorithm must be 'sha1', 'sha256', or 'sha512'")
    if timestamp < t0:
        raise ValueError("timestamp must be greater than or equal to t0")

    counter = (timestamp - t0) // period
    message = struct.pack(">Q", counter)
    digest = hmac.new(secret, message, getattr(hashlib, algorithm)).digest()

    offset = digest[-1] & 0x0F
    binary_code = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    code = binary_code % (10 ** digits)

    return f"{code:0{digits}d}"
