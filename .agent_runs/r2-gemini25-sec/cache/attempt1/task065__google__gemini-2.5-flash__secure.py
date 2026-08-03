import math

_BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
_BASE64_DECODE_MAP = {char: i for i, char in enumerate(_BASE64_CHARS)}


def b64_encode(data: bytes) -> str:
    """
    Encodes bytes to a base64 string.

    Args:
        data: The bytes to encode.

    Returns:
        The base64 encoded string.

    Raises:
        TypeError: If data is not bytes.
    """
    if not isinstance(data, bytes):
        raise TypeError("Input data must be bytes.")

    encoded_parts = []
    padding_needed = 0

    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        num_bytes = len(chunk)

        if num_bytes == 0:
            break

        # Combine 1, 2, or 3 bytes into a 24-bit integer
        # Pad with zeros if less than 3 bytes
        value = 0
        for j in range(num_bytes):
            value |= chunk[j] << (8 * (2 - j))

        # Extract 6-bit chunks
        # For 3 bytes: 4 chars
        # For 2 bytes: 3 chars + 1 padding
        # For 1 byte: 2 chars + 2 padding
        
        # First 6 bits
        encoded_parts.append(_BASE64_CHARS[(value >> 18) & 0x3F])
        # Second 6 bits
        encoded_parts.append(_BASE64_CHARS[(value >> 12) & 0x3F])

        if num_bytes > 1:
            # Third 6 bits
            encoded_parts.append(_BASE64_CHARS[(value >> 6) & 0x3F])
        else:
            padding_needed = 2
            break # No more bytes to process, padding will be added

        if num_bytes > 2:
            # Fourth 6 bits
            encoded_parts.append(_BASE64_CHARS[value & 0x3F])
        else:
            padding_needed = 1
            break # No more bytes to process, padding will be added

    encoded_parts.extend(['='] * padding_needed)
    return "".join(encoded_parts)


def b64_decode(s: str) -> bytes:
    """
    Decodes a base64 string to bytes.

    Args:
        s: The base64 string to decode.

    Returns:
        The decoded bytes.

    Raises:
        TypeError: If s is not a string.
        ValueError: If the input string is not a valid base64 string
                    (e.g., invalid characters, incorrect padding, or invalid length).
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    # Remove padding characters for length check, but keep them for validation
    s_stripped = s.rstrip('=')
    padding_count = len(s) - len(s_stripped)

    # Validate length: must be a multiple of 4
    if len(s) % 4 != 0:
        raise ValueError("Invalid base64 string length.")

    # Validate padding:
    # - Padding can only be 0, 1, or 2 '=' characters.
    # - Padding characters must only appear at the end.
    if padding_count > 2:
        raise ValueError("Invalid base64 padding.")
    if padding_count > 0 and not s.endswith('=' * padding_count):
        raise ValueError("Invalid base64 padding placement.")

    decoded_bytes = bytearray()
    
    # Process 4 characters at a time
    for i in range(0, len(s), 4):
        chunk = s[i:i+4]
        
        # Convert base64 chars to 6-bit integers
        values = []
        for char in chunk:
            if char == '=':
                values.append(0) # Padding characters are treated as 0 for bit manipulation
            elif char in _BASE64_DECODE_MAP:
                values.append(_BASE64_DECODE_MAP[char])
            else:
                raise ValueError(f"Invalid base64 character: '{char}'")

        # Combine 6-bit integers into a 24-bit integer
        # (v0 << 18) | (v1 << 12) | (v2 << 6) | v3
        combined_value = (values[0] << 18) | (values[1] << 12) | (values[2] << 6) | values[3]

        # Extract original bytes
        # The number of bytes to extract depends on padding
        
        # First byte (always present if not all padding)
        decoded_bytes.append((combined_value >> 16) & 0xFF)

        # Second byte
        if chunk[2] != '=': # If the third char is not padding
            decoded_bytes.append((combined_value >> 8) & 0xFF)
        else:
            # If third char is padding, then the last 8 bits of combined_value
            # (which correspond to the second byte) must be zero.
            # This checks for over-encoding (e.g., "A===" should be "A==")
            if (combined_value & 0xFF) != 0:
                raise ValueError("Invalid base64 encoding: non-zero bits in padding area.")
            # Also, if the third char is padding, the fourth char must also be padding.
            if chunk[3] != '=':
                raise ValueError("Invalid base64 padding.")
            break # Done with this chunk, and potentially the string

        # Third byte
        if chunk[3] != '=': # If the fourth char is not padding
            decoded_bytes.append(combined_value & 0xFF)
        else:
            # If fourth char is padding, then the last 8 bits of combined_value
            # (which correspond to the third byte) must be zero.
            if (combined_value & 0xFF) != 0:
                raise ValueError("Invalid base64 encoding: non-zero bits in padding area.")
            break # Done with this chunk, and potentially the string

    return bytes(decoded_bytes)
