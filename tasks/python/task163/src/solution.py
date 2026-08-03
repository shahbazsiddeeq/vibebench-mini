"""RFC 4648 Base32 codec implemented from scratch (no base64 module)."""

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_DECODE = {c: i for i, c in enumerate(_ALPHABET)}
# Mapping from number of leftover input bytes -> number of '=' pad chars.
_PAD_FOR_BYTES = {1: 6, 2: 4, 3: 3, 4: 1, 0: 0}
# Valid pad-char counts that can legally terminate a Base32 block.
_VALID_PADS = {0, 1, 3, 4, 6}


def base32_encode(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    data = bytes(data)
    out = []
    for i in range(0, len(data), 5):
        chunk = data[i:i + 5]
        n = len(chunk)
        buf = int.from_bytes(chunk + b"\x00" * (5 - n), "big")
        # 40-bit value; take 8 groups of 5 bits, most significant first.
        chars = [(buf >> (35 - 5 * j)) & 0x1F for j in range(8)]
        significant = {1: 2, 2: 4, 3: 5, 4: 7, 5: 8}[n]
        for j in range(8):
            out.append(_ALPHABET[chars[j]] if j < significant else "=")
    return "".join(out)


def base32_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("s must be str")
    if len(s) % 8 != 0:
        raise ValueError("input length must be a multiple of 8")
    if s == "":
        return b""
    s = s.upper()
    result = bytearray()
    for i in range(0, len(s), 8):
        block = s[i:i + 8]
        pad = 0
        # Padding may only be a trailing run of '='.
        while pad < 8 and block[7 - pad] == "=":
            pad += 1
        if "=" in block[: 8 - pad]:
            raise ValueError("misplaced padding character")
        if pad not in _VALID_PADS:
            raise ValueError("invalid amount of padding")
        buf = 0
        for c in block[: 8 - pad]:
            if c not in _DECODE:
                raise ValueError(f"invalid base32 character: {c!r}")
            buf = (buf << 5) | _DECODE[c]
        # Left-align to 40 bits.
        buf <<= 5 * pad
        nbytes = {0: 5, 1: 4, 3: 3, 4: 2, 6: 1}[pad]
        chunk = buf.to_bytes(5, "big")
        result.extend(chunk[:nbytes])
    return bytes(result)
