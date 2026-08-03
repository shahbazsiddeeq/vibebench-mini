"""RFC 4648 Base32 encoder and decoder."""

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_DECODE_TABLE = {char: index for index, char in enumerate(_ALPHABET)}
_DECODE_TABLE.update({char.lower(): index for index, char in enumerate(_ALPHABET)})

_VALID_PADDING = {0, 1, 3, 4, 6}


def base32_encode(data: bytes) -> str:
    """Encode bytes using RFC 4648 Base32 with padding."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    if not data:
        return ""

    output = []
    buffer = 0
    bits = 0

    for byte in data:
        buffer = (buffer << 8) | byte
        bits += 8

        while bits >= 5:
            bits -= 5
            output.append(_ALPHABET[(buffer >> bits) & 0x1F])

        if bits:
            buffer &= (1 << bits) - 1
        else:
            buffer = 0

    if bits:
        output.append(_ALPHABET[(buffer << (5 - bits)) & 0x1F])

    output.extend("=" * ((-len(output)) % 8))
    return "".join(output)


def base32_decode(s: str) -> bytes:
    """Decode a padded, case-insensitive RFC 4648 Base32 string."""
    if not isinstance(s, str):
        raise TypeError("s must be a str")

    if len(s) % 8 != 0:
        raise ValueError("Base32 input length must be a multiple of 8")

    first_padding = s.find("=")
    if first_padding == -1:
        encoded = s
        padding_count = 0
    else:
        encoded = s[:first_padding]
        padding = s[first_padding:]
        if any(char != "=" for char in padding):
            raise ValueError("padding must form a trailing run")
        padding_count = len(padding)

    if padding_count not in _VALID_PADDING:
        raise ValueError("invalid Base32 padding length")

    output = bytearray()
    buffer = 0
    bits = 0

    for char in encoded:
        try:
            value = _DECODE_TABLE[char]
        except KeyError:
            raise ValueError(f"invalid Base32 character: {char!r}") from None

        buffer = (buffer << 5) | value
        bits += 5

        while bits >= 8:
            bits -= 8
            output.append((buffer >> bits) & 0xFF)

        if bits:
            buffer &= (1 << bits) - 1
        else:
            buffer = 0

    if bits and buffer != 0:
        raise ValueError("non-zero unused bits in final Base32 character")

    return bytes(output)
