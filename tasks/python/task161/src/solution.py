"""Time-based One-Time Password generator (RFC 6238)."""

import hashlib
import hmac
import struct

_ALGOS = {"sha1": hashlib.sha1, "sha256": hashlib.sha256, "sha512": hashlib.sha512}


def _is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def totp(
    secret: bytes,
    timestamp: int,
    period: int = 30,
    digits: int = 6,
    algorithm: str = "sha1",
    t0: int = 0,
) -> str:
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes")
    for name, val in (("timestamp", timestamp), ("period", period),
                      ("digits", digits), ("t0", t0)):
        if not _is_int(val):
            raise TypeError(f"{name} must be int")
    if period < 1:
        raise ValueError("period must be >= 1")
    if not 1 <= digits <= 10:
        raise ValueError("digits must be in 1..10")
    if algorithm not in _ALGOS:
        raise ValueError("algorithm must be sha1, sha256, or sha512")
    if timestamp < t0:
        raise ValueError("timestamp must be >= t0")

    counter = (timestamp - t0) // period
    msg = struct.pack(">Q", counter)
    digest = hmac.new(bytes(secret), msg, _ALGOS[algorithm]).digest()
    offset = digest[-1] & 0x0F
    code = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    code %= 10 ** digits
    return str(code).zfill(digits)
