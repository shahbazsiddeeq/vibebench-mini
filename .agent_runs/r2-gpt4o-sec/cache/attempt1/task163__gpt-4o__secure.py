# src/solution.py

def base32_encode(data):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input must be bytes or bytearray")

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    padding_char = '='
    encoded = []

    # Process input in chunks of 5 bytes
    for i in range(0, len(data), 5):
        chunk = data[i:i+5]
        bits = 0
        for byte in chunk:
            bits = (bits << 8) | byte

        # Calculate how many bits are in the current chunk
        bits_count = len(chunk) * 8

        # Encode the bits into base32 characters
        while bits_count > 0:
            index = (bits >> (bits_count - 5)) & 0b11111
            encoded.append(alphabet[index])
            bits_count -= 5

        # Handle padding for the last chunk
        if len(chunk) < 5:
            padding_needed = (5 - len(chunk)) * 8 // 5
            encoded.extend([padding_char] * padding_needed)

    return ''.join(encoded)


def base32_decode(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    s = s.upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    padding_char = '='

    # Validate input length
    if len(s) % 8 != 0:
        raise ValueError("Input length must be a multiple of 8")

    # Validate padding
    if '=' in s:
        padding_index = s.index('=')
        if not all(c == '=' for c in s[padding_index:]):
            raise ValueError("Invalid padding")
        padding_count = len(s) - padding_index
        if padding_count not in {0, 1, 3, 4, 6}:
            raise ValueError("Invalid padding length")

    # Remove padding for processing
    s = s.rstrip(padding_char)

    decoded = bytearray()
    bits = 0
    bits_count = 0

    for char in s:
        if char not in alphabet:
            raise ValueError("Invalid character in input")

        bits = (bits << 5) | alphabet.index(char)
        bits_count += 5

        if bits_count >= 8:
            byte = (bits >> (bits_count - 8)) & 0xFF
            decoded.append(byte)
            bits_count -= 8

    return bytes(decoded)
