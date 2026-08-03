def base32_encode(data: bytes) -> str:
    """Encode bytes to Base32 string (RFC 4648)."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    
    if len(data) == 0:
        return ""
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    result = []
    
    # Process complete 5-byte groups
    i = 0
    while i + 5 <= len(data):
        # Convert 5 bytes to 40 bits
        chunk = data[i:i+5]
        bits = int.from_bytes(chunk, 'big')
        
        # Extract 8 groups of 5 bits
        for j in range(7, -1, -1):
            index = (bits >> (j * 5)) & 0x1F
            result.append(alphabet[index])
        
        i += 5
    
    # Handle remaining bytes (0-4 bytes)
    remaining = len(data) - i
    if remaining > 0:
        chunk = data[i:]
        # Pad chunk to 5 bytes for processing
        bits = int.from_bytes(chunk + b'\x00' * (5 - remaining), 'big')
        
        # Calculate how many output characters we need
        # 1 byte (8 bits) → 2 chars (10 bits, use 8)
        # 2 bytes (16 bits) → 4 chars (20 bits, use 16)
        # 3 bytes (24 bits) → 5 chars (25 bits, use 24)
        # 4 bytes (32 bits) → 7 chars (35 bits, use 32)
        num_chars = {1: 2, 2: 4, 3: 5, 4: 7}[remaining]
        
        for j in range(7, 7 - num_chars, -1):
            index = (bits >> (j * 5)) & 0x1F
            result.append(alphabet[index])
        
        # Add padding to make total length multiple of 8
        padding_needed = 8 - num_chars
        result.extend(['='] * padding_needed)
    
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
    
    # Validate padding count (must be 0, 1, 3, 4, or 6)
    if padding_count not in (0, 1, 3, 4, 6):
        raise ValueError(f"invalid padding count: {padding_count}")
    
    # Check for misplaced padding
    data_part = s[:len(s) - padding_count] if padding_count > 0 else s
    if '=' in data_part:
        raise ValueError("padding character '=' found in non-padding position")
    
    # Validate all non-padding characters are in alphabet (case-insensitive)
    for char in data_part:
        if char.upper() not in alphabet:
            raise ValueError(f"invalid character: {char}")
    
    result = []
    
    # Process in 8-character groups
    for i in range(0, len(s), 8):
        group = s[i:i+8]
        
        # Count padding in this group
        group_padding = sum(1 for c in group if c == '=')
        
        # Convert characters to indices
        bits = 0
        for j, char in enumerate(group):
            if char == '=':
                break
            index = alphabet.index(char.upper())
            bits = (bits << 5) | index
        
        # Determine how many bytes to extract based on padding
        if group_padding == 0:
            num_bytes = 5
            bits_to_use = 40
        elif group_padding == 1:
            num_bytes = 4
            bits_to_use = 35
            bits >>= 5  # Remove unused bits
        elif group_padding == 3:
            num_bytes = 3
            bits_to_use = 24
            bits >>= 15  # Remove unused bits
        elif group_padding == 4:
            num_bytes = 2
            bits_to_use = 20
            bits >>= 20  # Remove unused bits
        elif group_padding == 6:
            num_bytes = 1
            bits_to_use = 10
            bits >>= 30  # Remove unused bits
        else:
            raise ValueError(f"invalid padding in group: {group_padding}")
        
        # Extract bytes
        for j in range(num_bytes - 1, -1, -1):
            byte_val = (bits >> (j * 8)) & 0xFF
            result.append(byte_val)
    
    return bytes(result)
