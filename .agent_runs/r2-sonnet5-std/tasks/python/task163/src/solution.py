ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_CHAR_TO_VAL = {c: i for i, c in enumerate(ALPHABET)}
VALID_PAD_COUNTS = {0, 1, 3, 4, 6}


def base32_encode(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    data = bytes(data)
    if len(data) == 0:
        return ""

    result = []
    for i in range(0, len(data), 5):
        chunk = data[i:i + 5]
        chunk_len = len(chunk)
        # pad chunk to 5 bytes with zero bits
        padded = chunk + b"\x00" * (5 - chunk_len)
        bits = int.from_bytes(padded, "big")
        chars = []
        for shift in range(35, -1, -5):
            chars.append((bits >> shift) & 0x1F)

        # determine number of output chars based on chunk_len
        out_chars_map = {1: 2, 2: 4, 3: 5, 4: 7, 5: 8}
        n_out = out_chars_map[chunk_len]
        n_pad = 8 - n_out

        encoded_chars = "".join(ALPHABET[v] for v in chars[:n_out])
        result.append(encoded_chars + "=" * n_pad)

    return "".join(result)


def base32_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("s must be a str")

    if len(s) % 8 != 0:
        raise ValueError("Input length must be a multiple of 8")

    if len(s) == 0:
        return b""

    upper_s = s.upper()

    # find padding
    stripped = upper_s.rstrip("=")
    pad_count = len(upper_s) - len(stripped)

    if pad_count not in VALID_PAD_COUNTS:
        raise ValueError("Invalid padding count")

    # check no '=' in the non-padding part
    if "=" in stripped:
        raise ValueError("Misplaced padding character")

    # validate all characters in stripped are in alphabet
    for ch in stripped:
        if ch not in _CHAR_TO_VAL:
            raise ValueError(f"Invalid character: {ch}")

    # process in blocks of 8 chars
    result = bytearray()
    n_blocks = len(upper_s) // 8

    # map pad_count to expected number of output bytes for last block
    pad_to_bytes = {0: 5, 1: 4, 3: 3, 4: 2, 6: 1}

    for i in range(n_blocks):
        block = upper_s[i * 8:(i + 1) * 8]
        block_pad = len(block) - len(block.rstrip("="))
        block_stripped = block.rstrip("=")

        n_out_bytes = pad_to_bytes.get(block_pad, 5)

        # build bits
        bits = 0
        n_chars = len(block_stripped)
        for ch in block_stripped:
            bits = (bits << 5) | _CHAR_TO_VAL[ch]
        # pad bits to fill 40 bits total
        total_bits_used = n_chars * 5
        bits <<= (40 - total_bits_used)

        out_bytes = bits.to_bytes(5, "big")[:n_out_bytes]
        result.extend(out_bytes)

    return bytes(result)
