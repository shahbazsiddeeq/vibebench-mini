"""Base32 Codec (RFC 4648) implementation."""

# RFC 4648 Base32 alphabet
BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

# Create decode map (case-insensitive)
DECODE_MAP = {}
for i, char in enumerate(BASE32_ALPHABET):
    DECODE_MAP[char] = i
    DECODE_MAP[char.lower()] = i


def base32_encode(data: bytes) -> str:
    """
    Encode bytes to Base32 string (RFC 4648).
    
    Args:
        data: bytes or bytearray to encode
        
    Returns:
        Base32 encoded string with padding
        
    Raises:
        TypeError: if data is not bytes or bytearray
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    
    if len(data) == 0:
        return ""
    
    result = []
    
    # Process complete 5-byte groups (40 bits -> 8 characters)
    for i in range(0, len(data), 5):
        chunk = data[i:i+5]
        
        # Convert chunk to integer (big-endian)
        bits = 0
        for byte in chunk:
            bits = (bits << 8) | byte
        
        # Determine how many characters to output
        chunk_len = len(chunk)
        if chunk_len == 5:
            num_chars = 8
            num_padding = 0
        elif chunk_len == 4:
            num_chars = 7
            num_padding = 1
            bits <<= 8  # Pad with zeros on the right
        elif chunk_len == 3:
            num_chars = 5
            num_padding = 3
            bits <<= 16
        elif chunk_len == 2:
            num_chars = 4
            num_padding = 4
            bits <<= 24
        else:  # chunk_len == 1
            num_chars = 2
            num_padding = 6
            bits <<= 32
        
        # Extract 5-bit groups from left to right
        chars = []
        for j in range(num_chars):
            # Extract top 5 bits
            index = (bits >> (35 - j * 5)) & 0x1F
            chars.append(BASE32_ALPHABET[index])
        
        result.extend(chars)
        result.extend(['='] * num_padding)
    
    return ''.join(result)


def base32_decode(s: str) -> bytes:
    """
    Decode Base32 string to bytes (RFC 4648).
    
    Args:
        s: Base32 encoded string
        
    Returns:
        Decoded bytes
        
    Raises:
        TypeError: if s is not a string
        ValueError: if input is invalid Base32
    """
    if not isinstance(s, str):
        raise TypeError("input must be a string")
    
    if len(s) == 0:
        return b""
    
    # Validate length is multiple of 8
    if len(s) % 8 != 0:
        raise ValueError("input length must be a multiple of 8")
    
    # Count and validate padding
    padding_count = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == '=':
            padding_count += 1
        else:
            break
    
    # Valid padding counts: 0, 1, 3, 4, 6
    if padding_count not in (0, 1, 3, 4, 6):
        raise ValueError(f"invalid padding count: {padding_count}")
    
    # Validate no padding in the middle
    data_part = s[:len(s) - padding_count] if padding_count > 0 else s
    if '=' in data_part:
        raise ValueError("padding character '=' found in non-padding position")
    
    # Validate all data characters are in alphabet
    for char in data_part:
        if char not in DECODE_MAP:
            raise ValueError(f"invalid character: {char}")
    
    result = []
    
    # Process in 8-character groups
    for i in range(0, len(s), 8):
        chunk = s[i:i+8]
        
        # Count padding in this chunk
        chunk_padding = chunk.count('=')
        chunk_data = chunk[:8 - chunk_padding]
        
        # Convert characters to 40-bit integer
        bits = 0
        for char in chunk_data:
            bits = (bits << 5) | DECODE_MAP[char]
        
        # Determine how many bytes to output based on padding
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
        
        # Shift bits to align properly
        # We have len(chunk_data) * 5 bits
        # We need to extract num_bytes * 8 bits from the left
        total_bits = len(chunk_data) * 5
        
        # Extract bytes from left to right
        for j in range(num_bytes):
            # Extract top 8 bits
            byte_val = (bits >> (total_bits - 8 - j * 8)) & 0xFF
            result.append(byte_val)
    
    return bytes(result)
