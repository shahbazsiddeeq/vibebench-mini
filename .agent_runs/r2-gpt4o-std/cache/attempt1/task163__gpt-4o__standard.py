# src/solution.py

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
            index = (bits >> (bit_count - 5)) & 0x1F
            encoded.append(alphabet[index])
            bit_count -= 5

        # Add padding if necessary
        if len(chunk) < 5:
            padding_count = (5 - len(chunk)) * 8 // 5
            encoded.extend([padding] * padding_count)

    return ''.join(encoded)


def base32_decode(s):
    if not isinstance(s, str):
        raise TypeError("s must be a string")

    s = s.upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    padding = '='

    # Validate input
    if len(s) % 8 != 0:
        raise ValueError("Input length must be a multiple of 8")

    if any(c not in alphabet + padding for c in s):
        raise ValueError("Invalid character in input")

    if padding in s[:-8]:
        raise ValueError("Padding character '=' found in the middle of input")

    padding_count = s.count(padding)
    if padding_count not in (0, 1, 3, 4, 6):
        raise ValueError("Invalid number of padding characters")

    decoded = bytearray()
    bits = 0
    bit_count = 0

    for char in s:
        if char == padding:
            break

        bits = (bits << 5) | alphabet.index(char)
        bit_count += 5

        if bit_count >= 8:
            byte = (bits >> (bit_count - 8)) & 0xFF
            decoded.append(byte)
            bit_count -= 8

    return bytes(decoded)
