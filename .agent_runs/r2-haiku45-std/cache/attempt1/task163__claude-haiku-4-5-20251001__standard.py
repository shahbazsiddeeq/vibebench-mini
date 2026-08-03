"""RFC 4648 Base32 Codec implementation."""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
PADDING = "="


def base32_encode(data: bytes) -> str:
    """
    Encode bytes to Base32 string according to RFC 4648.
    
    Args:
        data: bytes or bytearray to encode
        
    Returns:
        Base32 encoded string with '=' padding
        
    Raises:
        TypeError: if data is not bytes or bytearray
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    
    if len(data) == 0:
        return ""
    
    result = []
    
    # Process input in groups of 5 bytes (40 bits)
    i = 0
    while i < len(data):
        # Get up to 5 bytes
        chunk = data[i:i+5]
        i += 5
        
        # Convert bytes to a single integer
        num = 0
        for byte in chunk:
            num = (num << 8) | byte
        
        # Determine how many bits we have
        bit_count = len(chunk) * 8
        
        # Pad to the right with zeros to make it a multiple of 5 bits
        # We need to extract 5-bit groups from the left
        num <<= (40 - bit_count)  # Shift left to align to 40 bits
        
        # Extract 8 5-bit values (even if some are padding)
        for j in range(8):
            if bit_count >= 5:
                # Extract the top 5 bits
                index = (num >> (35 - j * 5)) & 0x1F
                result.append(ALPHABET[index])
                bit_count -= 5
            else:
                # Padding character
                result.append(PADDING)
    
    return "".join(result)


def base32_decode(s: str) -> bytes:
    """
    Decode Base32 string to bytes according to RFC 4648.
    
    Args:
        s: Base32 encoded string (case insensitive)
        
    Returns:
        Decoded bytes
        
    Raises:
        TypeError: if s is not a str
        ValueError: if input is invalid (bad length, bad characters, bad padding)
    """
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    
    # Check length is multiple of 8
    if len(s) % 8 != 0:
        raise ValueError("input length must be a multiple of 8")
    
    # Convert to uppercase for processing
    s = s.upper()
    
    # Count and validate padding
    padding_count = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == PADDING:
            padding_count += 1
        else:
            break
    
    # Valid padding counts: 0, 1, 3, 4, 6
    if padding_count not in (0, 1, 3, 4, 6):
        raise ValueError("invalid number of padding characters")
    
    # Check that padding only appears at the end
    if padding_count > 0:
        if s[len(s) - padding_count - 1] == PADDING:
            raise ValueError("padding characters must be at the end")
    
    # Validate all non-padding characters are in alphabet
    for i in range(len(s) - padding_count):
        if s[i] not in ALPHABET:
            raise ValueError(f"invalid character in input: {s[i]}")
    
    if len(s) == 0:
        return b""
    
    # Decode: convert each character to its 5-bit value
    result = []
    bit_buffer = 0
    bit_count = 0
    
    for i in range(len(s) - padding_count):
        char = s[i]
        value = ALPHABET.index(char)
        
        # Add 5 bits to buffer
        bit_buffer = (bit_buffer << 5) | value
        bit_count += 5
        
        # Extract complete bytes (8 bits)
        while bit_count >= 8:
            bit_count -= 8
            byte_val = (bit_buffer >> bit_count) & 0xFF
            result.append(byte_val)
    
    return bytes(result)
