"""RFC 6238 Time-based One-Time Password generation."""

import hashlib
import hmac
import struct


_ALGORITHMS = {
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def totp(
    secret: bytes,
    timestamp: int,
    period: int = 30,
    digits: int = 6,
    algorithm: str = "sha1",
    t0: int = 0,
) -> str:
    """Generate a TOTP code according to RFC 6238 and RFC 4226."""
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")

    for name, value in (
        ("timestamp", timestamp),
        ("period", period),
        ("digits", digits),
        ("t0", t0),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int")

    if period < 1:
        raise ValueError("period must be at least 1")
    if not 1 <= digits <= 10:
        raise ValueError("digits must be between 1 and 10")
    if not isinstance(algorithm, str) or algorithm not in _ALGORITHMS:
        raise ValueError("algorithm must be 'sha1', 'sha256', or 'sha512'")
    if timestamp < t0:
        raise ValueError("timestamp must not be earlier than t0")

    counter = (timestamp - t0) // period
    if counter > 0xFFFFFFFFFFFFFFFF:
        raise ValueError("counter exceeds the 8-byte unsigned integer range")

    message = struct.pack(">Q", counter)
    digest = hmac.new(secret, message, _ALGORITHMS[algorithm]).digest()

    offset = digest[-1] & 0x0F
    binary_code = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    code = binary_code % (10 ** digits)

    return f"{code:0{digits}d}"
