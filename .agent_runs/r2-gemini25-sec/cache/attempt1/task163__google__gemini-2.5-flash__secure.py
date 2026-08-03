import math

_BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_BASE32_DECODE_MAP = {char: i for i, char in enumerate(_BASE32_ALPHABET)}


def base32_encode(data: bytes) -> str:
    """
    Encodes bytes into a Base32 string according to RFC 4648.

    Args:
        data: The bytes to encode.

    Returns:
        The Base32 encoded string.

    Raises:
        TypeError: If `data` is not bytes or bytearray.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input data must be bytes or bytearray.")

    if not data:
        return ""

    encoded_parts = []
    # Process input in groups of 5 bytes (40 bits)
    for i in range(0, len(data), 5):
        chunk = data[i : i + 5]
        num_bytes = len(chunk)
        # Combine bytes into a 40-bit integer (or fewer if chunk is short)
        # Shift each byte into its position in the 40-bit integer
        # Example: b1 b2 b3 b4 b5
        # (b1 << 32) | (b2 << 24) | (b3 << 16) | (b4 << 8) | b5
        # This handles chunks shorter than 5 bytes by effectively padding with zeros
        # on the right, which is correct for bit manipulation.
        bits = 0
        for j in range(num_bytes):
            bits |= chunk[j] << (8 * (4 - j))  # Shift to the left-most positions

        # Extract 8 5-bit characters from the 40-bit integer
        # The number of output characters depends on the input chunk size
        # 5 bytes -> 8 chars
        # 4 bytes -> 7 chars
        # 3 bytes -> 5 chars
        # 2 bytes -> 4 chars
        # 1 byte  -> 2 chars
        num_output_chars = math.ceil(num_bytes * 8 / 5)

        for k in range(8):
            if k < num_output_chars:
                # Extract 5 bits from the most significant end
                # (bits >> (35 - k * 5)) & 0x1F
                # For k=0, (bits >> 35) & 0x1F
                # For k=1, (bits >> 30) & 0x1F
                # ...
                # For k=7, (bits >> 0) & 0x1F
                char_index = (bits >> (35 - k * 5)) & 0x1F
                encoded_parts.append(_BASE32_ALPHABET[char_index])
            else:
                encoded_parts.append("=")

    return "".join(encoded_parts)


def base32_decode(s: str) -> bytes:
    """
    Decodes a Base32 string into bytes according to RFC 4648.

    Args:
        s: The Base32 encoded string.

    Returns:
        The decoded bytes.

    Raises:
        TypeError: If `s` is not a string.
        ValueError: If the input is invalid (e.g., incorrect length, invalid characters,
                    malformed padding).
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    if not s:
        return b""

    # Validate length
    if len(s) % 8 != 0:
        raise ValueError("Input string length must be a multiple of 8.")

    # Find padding and validate its position
    padding_start = len(s)
    for i in range(len(s)):
        if s[i] == '=':
            padding_start = i
            break

    # All characters before padding must be in the alphabet
    for char in s[:padding_start]:
        if char.upper() not in _BASE32_DECODE_MAP:
            raise ValueError(f"Invalid character '{char}' found in Base32 string.")

    # All characters after padding_start must be '='
    if any(char != '=' for char in s[padding_start:]):
        raise ValueError("Padding character '=' can only appear at the end.")

    num_padding_chars = len(s) - padding_start
    # Valid padding counts: 0, 1, 3, 4, 6
    if num_padding_chars not in {0, 1, 3, 4, 6}:
        raise ValueError(f"Invalid number of padding characters: {num_padding_chars}.")

    # Remove padding for decoding
    s_stripped = s[:padding_start]

    decoded_bytes = bytearray()
    # Process input in groups of 8 characters (40 bits)
    for i in range(0, len(s_stripped), 8):
        chunk_chars = s_stripped[i : i + 8]
        num_chars_in_chunk = len(chunk_chars)

        # If a chunk is shorter than 8, it means it's the last chunk before padding
        # and we need to adjust the expected number of bits.
        # This should only happen if padding was removed, so num_chars_in_chunk
        # will be 8, 7, 5, 4, or 2.
        if num_chars_in_chunk == 0:
            continue # Should not happen with valid input, but for safety

        # Combine 5-bit characters into a 40-bit integer
        bits = 0
        for j in range(num_chars_in_chunk):
            char_val = _BASE32_DECODE_MAP[chunk_chars[j].upper()]
            bits |= char_val << (35 - j * 5) # Shift to the left-most positions

        # Determine how many bytes to extract based on the number of characters
        # 8 chars -> 5 bytes
        # 7 chars -> 4 bytes
        # 5 chars -> 3 bytes
        # 4 chars -> 2 bytes
        # 2 chars -> 1 byte
        num_output_bytes = (num_chars_in_chunk * 5) // 8

        for k in range(num_output_bytes):
            # Extract 8 bits from the most significant end
            byte_val = (bits >> (32 - k * 8)) & 0xFF
            decoded_bytes.append(byte_val)

    return bytes(decoded_bytes)
