"""RFC 4648 Base32 encoder and decoder."""

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_DECODE_TABLE = {
    char: index
    for index, upper in enumerate(_ALPHABET)
    for char in (upper, upper.lower())
}
_VALID_PADDING = {0, 1, 3, 4, 6}


def base32_encode(data: bytes) -> str:
    """Encode bytes using padded RFC 4648 Base32."""
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
            buffer &= (1 << bits) - 1

    if bits:
        output.append(_ALPHABET[(buffer << (5 - bits)) & 0x1F])

    output.extend("=" * ((-len(output)) % 8))
    return "".join(output)


def base32_decode(s: str) -> bytes:
    """Decode a strictly padded, case-insensitive RFC 4648 Base32 string."""
    if not isinstance(s, str):
        raise TypeError("s must be a str")

    if len(s) % 8 != 0:
        raise ValueError("Base32 input length must be a multiple of 8")

    if not s:
        return b""

    first_padding = s.find("=")
    if first_padding == -1:
        encoded = s
        padding_count = 0
    else:
        encoded = s[:first_padding]
        padding = s[first_padding:]
        if any(char != "=" for char in padding):
            raise ValueError("padding must be a trailing run")
        padding_count = len(padding)

    if padding_count not in _VALID_PADDING:
        raise ValueError("invalid Base32 padding length")

    output = bytearray()
    buffer = 0
    bits = 0

    for char in encoded:
        value = _DECODE_TABLE.get(char)
        if value is None:
            raise ValueError("invalid Base32 character")

        buffer = (buffer << 5) | value
        bits += 5

        while bits >= 8:
            bits -= 8
            output.append((buffer >> bits) & 0xFF)
            buffer &= (1 << bits) - 1

    # RFC 4648 requires unused bits in the final symbol to be zero.
    if buffer != 0:
        raise ValueError("non-zero unused bits in final Base32 symbol")

    return bytes(output)
