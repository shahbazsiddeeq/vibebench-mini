"""
TOTP Code Generator (RFC 6238 / RFC 4226)

Implements a secure, standard-library-only Time-based One-Time Password
generator with strict input validation.
"""

import hashlib
import hmac
import struct

_ALLOWED_ALGORITHMS = {
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def _is_strict_int(value: object) -> bool:
    """Return True if value is an int and not a bool."""
    return isinstance(value, int) and not isinstance(value, bool)


def totp(
    secret: bytes,
    timestamp: int,
    period: int = 30,
    digits: int = 6,
    algorithm: str = "sha1",
    t0: int = 0,
) -> str:
    """
    Compute a TOTP code per RFC 6238.

    Args:
        secret: shared secret key as bytes/bytearray.
        timestamp: unix timestamp (seconds) as int.
        period: time step size in seconds (default 30).
        digits: number of digits in the resulting code (1-10).
        algorithm: one of "sha1", "sha256", "sha512".
        t0: unix epoch offset (default 0).

    Returns:
        Zero-padded decimal string of length `digits`.

    Raises:
        TypeError: if types are invalid.
        ValueError: if values are out of allowed ranges.
    """
    # --- Type validation ---
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes or bytearray")

    if not _is_strict_int(timestamp):
        raise TypeError("timestamp must be an int")
    if not _is_strict_int(period):
        raise TypeError("period must be an int")
    if not _is_strict_int(digits):
        raise TypeError("digits must be an int")
    if not _is_strict_int(t0):
        raise TypeError("t0 must be an int")

    if not isinstance(algorithm, str):
        raise TypeError("algorithm must be a str")

    # --- Value validation ---
    if period < 1:
        raise ValueError("period must be >= 1")

    if digits < 1 or digits > 10:
        raise ValueError("digits must be between 1 and 10 inclusive")

    if algorithm not in _ALLOWED_ALGORITHMS:
        raise ValueError(f"algorithm must be one of {sorted(_ALLOWED_ALGORITHMS)}")

    if timestamp < t0:
        raise ValueError("timestamp must be >= t0")

    # --- Core computation ---
    counter = (timestamp - t0) // period
    msg = struct.pack(">Q", counter)

    secret_bytes = bytes(secret)
    hash_func = _ALLOWED_ALGORITHMS[algorithm]
    hmac_digest = hmac.new(secret_bytes, msg, hash_func).digest()

    offset = hmac_digest[-1] & 0x0F
    truncated = hmac_digest[offset : offset + 4]

    code_int = struct.unpack(">I", truncated)[0] & 0x7FFFFFFF
    code_int %= 10 ** digits

    return str(code_int).zfill(digits)
