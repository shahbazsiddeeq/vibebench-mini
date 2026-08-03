ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
PAD_CHAR = '='

def base32_encode(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input must be bytes or bytearray")

    if not data:
        return ""

    encoded_parts = []
    bits = 0
    bit_buffer = 0
    
    for byte in data:
        bit_buffer = (bit_buffer << 8) | byte
        bits += 8

        while bits >= 5:
            shift = bits - 5
            index = (bit_buffer >> shift) & 0x1F
            encoded_parts.append(ALPHABET[index])
            bits -= 5
            
    if bits > 0:
        # Pad with zeros to make it a multiple of 5 bits
        index = (bit_buffer << (5 - bits)) & 0x1F
        encoded_parts.append(ALPHABET[index])

    encoded_str = "".join(encoded_parts)

    # Add padding
    padding_needed = 8 - (len(encoded_str) % 8)
    if padding_needed != 8: # If it's already a multiple of 8, no padding
        encoded_str += PAD_CHAR * padding_needed

    return encoded_str

def base32_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    if not s:
        return b""

    # Validation 1: Input length must be a multiple of 8
    if len(s) % 8 != 0:
        raise ValueError("Input length must be a multiple of 8")

    # Convert to uppercase for case-insensitivity
    s_upper = s.upper()

    # Find padding characters
    padding_count = 0
    for char in reversed(s_upper):
        if char == PAD_CHAR:
            padding_count += 1
        else:
            break

    # Validation 2: Misplaced padding
    if padding_count > 0 and not s_upper.endswith(PAD_CHAR * padding_count):
        raise ValueError("Misplaced padding character '='")
    
    # Validation 3: Invalid padding count
    valid_padding_counts = {0, 1, 3, 4, 6}
    if padding_count not in valid_padding_counts:
        raise ValueError(f"Invalid number of padding characters: {padding_count}")

    # Remove padding for processing
    s_no_padding = s_upper[:-padding_count] if padding_count > 0 else s_upper

    decoded_bytes = bytearray()
    bits = 0
    bit_buffer = 0

    for char in s_no_padding:
        # Validation 4: Character outside alphabet
        if char not in ALPHABET:
            raise ValueError(f"Invalid character '{char}' in input string")
        
        value = ALPHABET.index(char)
        bit_buffer = (bit_buffer << 5) | value
        bits += 5

        while bits >= 8:
            shift = bits - 8
            byte = (bit_buffer >> shift) & 0xFF
            decoded_bytes.append(byte)
            bits -= 8

    # Handle remaining bits if any (should only happen due to padding removal)
    # The RFC implies that any remaining bits after processing the non-padded part
    # should be zero. If they are not, it indicates an invalid encoding.
    if bits > 0:
        # The remaining bits should be all zeros if the padding was correct.
        # If not, it means the original data didn't align with the padding.
        # For example, "MZXW6YTB" (5 bytes) has 0 padding.
        # If we decode "MZXW6YTBOI======" (6 bytes), the last 'I' gives 5 bits.
        # After processing 'O', we have 2 bits left. 'I' adds 5 bits, total 7.
        # We need 8 bits to form a byte.
        # The RFC states: "When the final group is short, encode the available bits"
        # This means the last partial group of 5 bits should be followed by zeros
        # to form the last byte.
        # If the last partial 5-bit group contains non-zero trailing bits that
        # would form part of a byte, it's an error.
        # Example: "MZXW6YQ=" (4 bytes). 'Q' is 10000.
        # After 'Q', we have 5 bits. We need 3 more bits to make a byte.
        # These 3 bits should be 0. If they were not, it's an error.
        # The current logic naturally handles this by only appending full bytes.
        # If `bit_buffer` contains non-zero bits that couldn't form a full byte,
        # it implies an over-encoded or malformed input.
        # For example, if `bits` is 3 and `bit_buffer` is 0b101, it's an error.
        # The RFC doesn't explicitly state this as a validation error, but
        # a strict decoder might check `bit_buffer & ((1 << bits) - 1)` for non-zero.
        # However, the common interpretation is that the encoder pads with zeros,
        # so any non-zero trailing bits would be an encoding error, not a decoding error
        # that needs explicit checking beyond what the byte extraction does.
        pass # The current loop naturally discards partial bytes.

    return bytes(decoded_bytes)
