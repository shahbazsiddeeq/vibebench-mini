"""
RFC 4648 Base32 codec implemented from scratch (no `base64` module).

Provides:
    base32_encode(data: bytes) -> str
    base32_decode(s: str) -> bytes

Security notes:
- Strict type checking on inputs (TypeError for wrong types).
- Strict validation of decode input (ValueError for malformed encodings):
    * length must be a multiple of 8
    * only characters from the RFC 4648 alphabet (case-insensitive) or
      trailing '=' padding are allowed
    * '=' may only appear as a valid trailing run
    * padding length must be one of {0, 1, 3, 4, 6}
- No use of eval/exec, no external data execution, no randomness needed here.
"""

from __future__ import annotations

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_ALPHABET_INDEX = {ch: idx for idx, ch in enumerate(_ALPHABET)}

# Mapping from number of valid (non-padding) data bytes in the final 5-byte
# group to number of significant base32 characters in the 8-char output.
_VALID_CHARS_FOR_CHUNK_LEN = {1: 2, 2: 4, 3: 5, 4: 7, 5: 8}

# Mapping from number of '=' padding chars (in an 8-char block) to number
# of decoded bytes that block represents.
_PAD_TO_NBYTES = {0: 5, 1: 4, 3: 3, 4: 2, 6: 1}

_VALID_PAD_LENGTHS = frozenset(_PAD_TO_NBYTES.keys())


def base32_encode(data: bytes) -> str:
    """Encode bytes to an RFC 4648 Base32 string."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    if len(data) == 0:
        return ""

    data = bytes(data)
    out_chars = []

    for i in range(0, len(data), 5):
        chunk = data[i:i + 5]
        chunk_len = len(chunk)

        bits = int.from_bytes(chunk, "big")
        # Left-pad the bits so we always work with a 40-bit value.
        bits <<= (5 - chunk_len) * 8

        chars = []
        for j in range(8):
            shift = 35 - j * 5
            index = (bits >> shift) & 0x1F
            chars.append(_ALPHABET[index])

        valid_chars = _VALID_CHARS_FOR_CHUNK_LEN[chunk_len]
        for k in range(valid_chars, 8):
            chars[k] = "="

        out_chars.append("".join(chars))

    return "".join(out_chars)


def base32_decode(s: str) -> bytes:
    """Decode an RFC 4648 Base32 string to bytes. Case-insensitive."""
    if not isinstance(s, str):
        raise TypeError("s must be a str")

    if len(s) == 0:
        return b""

    if len(s) % 8 != 0:
        raise ValueError("Base32 input length must be a multiple of 8")

    s_upper = s.upper()

    stripped = s_upper.rstrip("=")
    pad_len = len(s_upper) - len(stripped)

    if pad_len not in _VALID_PAD_LENGTHS:
        raise ValueError("Invalid padding length")

    # '=' must not appear anywhere except as the trailing run.
    if "=" in stripped:
        raise ValueError("'=' padding character misplaced")

    # Validate all non-padding characters are in the alphabet.
    for ch in stripped:
        if ch not in _ALPHABET_INDEX:
            raise ValueError(f"Invalid Base32 character: {ch!r}")

    result = bytearray()

    for i in range(0, len(s_upper), 8):
        block = s_upper[i:i + 8]
        block_stripped = block.rstrip("=")
        pad = 8 - len(block_stripped)

        if pad not in _VALID_PAD_LENGTHS:
            raise ValueError("Invalid padding length in block")

        bits = 0
        for ch in block_stripped:
            bits = (bits << 5) | _ALPHABET_INDEX[ch]

        total_bits = len(block_stripped) * 5
        bits <<= (40 - total_bits)

        n_bytes = _PAD_TO_NBYTES[pad]
        block_bytes = bits.to_bytes(5, "big")[:n_bytes]
        result.extend(block_bytes)

    return bytes(result)
