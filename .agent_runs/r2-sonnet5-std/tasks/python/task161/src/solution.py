import hmac
import hashlib
import struct


def totp(secret: bytes, timestamp: int, period: int = 30,
          digits: int = 6, algorithm: str = "sha1", t0: int = 0) -> str:
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")

    for name, value in (("timestamp", timestamp), ("period", period),
                        ("digits", digits), ("t0", t0)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int")

    if period < 1:
        raise ValueError("period must be >= 1")
    if not (1 <= digits <= 10):
        raise ValueError("digits must be between 1 and 10 inclusive")
    if algorithm not in ("sha1", "sha256", "sha512"):
        raise ValueError("algorithm must be one of 'sha1', 'sha256', 'sha512'")
    if timestamp < t0:
        raise ValueError("timestamp must be >= t0")

    counter = (timestamp - t0) // period
    msg = struct.pack(">Q", counter)

    digestmod = getattr(hashlib, algorithm)
    hmac_digest = hmac.new(bytes(secret), msg, digestmod).digest()

    offset = hmac_digest[-1] & 0x0F
    truncated = hmac_digest[offset:offset + 4]
    code_int = struct.unpack(">I", truncated)[0] & 0x7FFFFFFF
    code = code_int % (10 ** digits)

    return str(code).zfill(digits)
