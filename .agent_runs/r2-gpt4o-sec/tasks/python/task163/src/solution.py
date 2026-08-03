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
            if bits_count >= 5:
                index = (bits >> (bits_count - 5)) & 0b11111
                bits_count -= 5
            else:
                index = (bits << (5 - bits_count)) & 0b11111
                bits_count = 0
            encoded.append(alphabet[index])

        # Add padding if necessary
        if len(chunk) < 5:
            padding_length = (5 - len(chunk)) * 8 // 5
            encoded.extend([padding_char] * padding_length)

    return ''.join(encoded)


def base32_decode(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    s = s.upper()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    padding_char = '='
    decoded = bytearray()

    # Validate input
    if len(s) % 8 != 0:
        raise ValueError("Input length must be a multiple of 8")

    padding_index = s.find(padding_char)
    if padding_index != -1:
        if not all(c == padding_char for c in s[padding_index:]):
            raise ValueError("Invalid padding")
        if len(s) - padding_index not in {0, 1, 3, 4, 6}:
            raise ValueError("Invalid number of padding characters")

    # Remove padding for processing
    s = s.rstrip(padding_char)

    # Process input in chunks of 8 characters
    for i in range(0, len(s), 8):
        chunk = s[i:i+8]
        bits = 0
        bits_count = 0

        for char in chunk:
            if char not in alphabet:
                raise ValueError("Invalid character in input")
            bits = (bits << 5) | alphabet.index(char)
            bits_count += 5

        # Extract bytes from bits
        while bits_count >= 8:
            byte = (bits >> (bits_count - 8)) & 0xFF
            decoded.append(byte)
            bits_count -= 8

    return bytes(decoded)
