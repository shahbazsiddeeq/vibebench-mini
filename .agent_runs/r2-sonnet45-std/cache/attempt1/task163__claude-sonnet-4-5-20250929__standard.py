def base32_encode(data: bytes) -> str:
    """Encode bytes to Base32 string (RFC 4648)."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    
    if len(data) == 0:
        return ""
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    result = []
    
    # Process complete 5-byte groups
    for i in range(0, len(data), 5):
        chunk = data[i:i+5]
        chunk_len = len(chunk)
        
        # Pad chunk to 5 bytes for processing
        padded_chunk = chunk + b'\x00' * (5 - chunk_len)
        
        # Convert to 40-bit integer
        bits = int.from_bytes(padded_chunk, 'big')
        
        # Extract 8 groups of 5 bits each
        chars = []
        for j in range(8):
            # Extract 5 bits from position (35 - j*5) to (39 - j*5)
            shift = 35 - j * 5
            index = (bits >> shift) & 0x1F
            chars.append(alphabet[index])
        
        # Determine how many characters to keep based on input length
        if chunk_len == 5:
            result.extend(chars)
        elif chunk_len == 4:
            # 4 bytes = 32 bits → 7 chars (35 bits used, 5 bits padding)
            result.extend(chars[:7])
            result.append('=')
        elif chunk_len == 3:
            # 3 bytes = 24 bits → 5 chars (25 bits used, 15 bits padding)
            result.extend(chars[:5])
            result.extend(['=', '=', '='])
        elif chunk_len == 2:
            # 2 bytes = 16 bits → 4 chars (20 bits used, 20 bits padding)
            result.extend(chars[:4])
            result.extend(['=', '=', '=', '='])
        elif chunk_len == 1:
            # 1 byte = 8 bits → 2 chars (10 bits used, 30 bits padding)
            result.extend(chars[:2])
            result.extend(['=', '=', '=', '=', '=', '='])
    
    return ''.join(result)


def base32_decode(s: str) -> bytes:
    """Decode Base32 string to bytes (RFC 4648)."""
    if not isinstance(s, str):
        raise TypeError("input must be a string")
    
    if len(s) == 0:
        return b""
    
    # Check length is multiple of 8
    if len(s) % 8 != 0:
        raise ValueError("input length must be a multiple of 8")
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    
    # Count and validate padding
    padding_count = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == '=':
            padding_count += 1
        else:
            break
    
    # Validate padding count
    if padding_count not in [0, 1, 3, 4, 6]:
        raise ValueError(f"invalid padding count: {padding_count}")
    
    # Validate no padding in the middle
    if '=' in s[:len(s) - padding_count]:
        raise ValueError("padding character '=' found in middle of input")
    
    # Validate all non-padding characters are in alphabet
    data_part = s[:len(s) - padding_count]
    for char in data_part:
        if char.upper() not in alphabet:
            raise ValueError(f"invalid character: {char}")
    
    result = []
    
    # Process in 8-character groups
    for i in range(0, len(s), 8):
        chunk = s[i:i+8]
        
        # Count padding in this chunk
        chunk_padding = chunk.count('=')
        
        # Convert characters to 40-bit integer
        bits = 0
        for j, char in enumerate(chunk):
            if char == '=':
                break
            index = alphabet.index(char.upper())
            bits = (bits << 5) | index
        
        # Shift to account for padding
        bits <<= (chunk_padding * 5)
        
        # Determine how many bytes to extract
        if chunk_padding == 0:
            num_bytes = 5
        elif chunk_padding == 1:
            num_bytes = 4
        elif chunk_padding == 3:
            num_bytes = 3
        elif chunk_padding == 4:
            num_bytes = 2
        elif chunk_padding == 6:
            num_bytes = 1
        else:
            raise ValueError(f"invalid padding in chunk: {chunk_padding}")
        
        # Extract bytes
        byte_data = bits.to_bytes(5, 'big')
        result.extend(byte_data[:num_bytes])
    
    return bytes(result)
