def base32_encode(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    
    if len(data) == 0:
        return ""
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    result = []
    
    # Process input in 5-byte chunks
    i = 0
    while i < len(data):
        chunk = data[i:i+5]
        i += 5
        
        # Convert chunk to bits
        bits = 0
        for byte in chunk:
            bits = (bits << 8) | byte
        
        # Determine how many bits we have
        num_bits = len(chunk) * 8
        
        # Pad bits to multiple of 5 on the right
        bits <<= (40 - num_bits)
        
        # Extract 5-bit groups
        for j in range(8):
            if j * 5 < num_bits:
                index = (bits >> (35 - j * 5)) & 0x1f
                result.append(alphabet[index])
            else:
                result.append('=')
    
    return ''.join(result)


def base32_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    
    # Check length is multiple of 8
    if len(s) % 8 != 0:
        raise ValueError("input length must be a multiple of 8")
    
    if len(s) == 0:
        return b""
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    s_upper = s.upper()
    
    # Count padding
    padding_count = 0
    for i in range(len(s_upper) - 1, -1, -1):
        if s_upper[i] == '=':
            padding_count += 1
        else:
            break
    
    # Validate padding count
    if padding_count not in (0, 1, 3, 4, 6):
        raise ValueError("invalid padding count")
    
    # Check for misplaced padding
    for i in range(len(s_upper) - padding_count):
        if s_upper[i] == '=':
            raise ValueError("padding must be at the end")
    
    # Validate characters
    for i in range(len(s_upper) - padding_count):
        if s_upper[i] not in alphabet:
            raise ValueError(f"invalid character: {s_upper[i]}")
    
    result = []
    
    # Process in 8-character chunks
    for i in range(0, len(s_upper), 8):
        chunk = s_upper[i:i+8]
        
        # Convert characters to 5-bit values
        bits = 0
        num_chars = 0
        for char in chunk:
            if char == '=':
                break
            bits = (bits << 5) | alphabet.index(char)
            num_chars += 1
        
        # Determine how many bits are valid
        num_bits = num_chars * 5
        
        # Shift to align to byte boundary and extract bytes
        bits <<= (40 - num_bits)
        
        # Extract complete bytes
        num_bytes = num_bits // 8
        for j in range(num_bytes):
            byte_val = (bits >> (32 - j * 8)) & 0xff
            result.append(byte_val)
    
    return bytes(result)
