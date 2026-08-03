def base32_encode(data):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    encoded = []
    padding = '='

    # Process input in chunks of 5 bytes
    for i in range(0, len(data), 5):
        chunk = data[i:i+5]
        bits = 0
        for byte in chunk:
            bits = (bits << 8) | byte

        # Calculate how many bits are in the current chunk
        bit_count = len(chunk) * 8

        # Encode the bits into base32 characters
        while bit_count > 0:
            if bit_count >= 5:
                index = (bits >> (bit_count - 5)) & 0x1F
                bit_count -= 5
            else:
                index = (bits << (5 - bit_count)) & 0x1F
                bit_count = 0
            encoded.append(alphabet[index])

        # Add padding if necessary
        if len(chunk) < 5:
            padding_count = (5 - len(chunk)) * 8 // 5
            encoded.extend([padding] * padding_count)

    return ''.join(encoded)


def base32_decode(s):
    if not isinstance(s, str):
        raise TypeError("s must be a str")

    s = s.upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    padding = '='

    if len(s) % 8 != 0:
        raise ValueError("Input length must be a multiple of 8")

    # Check for valid padding
    if '=' in s:
        if not s.endswith('='):
            raise ValueError("Padding must be at the end")
        padding_count = len(s) - len(s.rstrip('='))
        if padding_count not in (0, 1, 3, 4, 6):
            raise ValueError("Invalid padding length")

    decoded = bytearray()
    bits = 0
    bit_count = 0

    for char in s.rstrip('='):
        if char not in alphabet:
            raise ValueError("Invalid character in input")

        bits = (bits << 5) | alphabet.index(char)
        bit_count += 5

        if bit_count >= 8:
            byte = (bits >> (bit_count - 8)) & 0xFF
            decoded.append(byte)
            bit_count -= 8

    return bytes(decoded)
