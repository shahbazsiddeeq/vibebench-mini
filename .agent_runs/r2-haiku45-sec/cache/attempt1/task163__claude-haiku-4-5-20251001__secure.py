"""RFC 4648 Base32 codec implementation."""

import string
from typing import Union

# RFC 4648 Base32 alphabet
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
PADDING_CHAR = "="

# Valid padding lengths for each input length modulo 5
# 0 bytes -> 0 padding, 1 byte -> 6 padding, 2 bytes -> 4 padding,
# 3 bytes -> 3 padding, 4 bytes -> 1 padding
VALID_PADDING_COUNTS = {0, 1, 3, 4, 6}


def base32_encode(data: Union[bytes, bytearray]) -> str:
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
    for i in range(0, len(data), 5):
        chunk = data[i:i+5]
        
        # Convert chunk to a single integer
        value = 0
        for byte in chunk:
            value = (value << 8) | byte
        
        # Determine how many bits we have
        bits = len(chunk) * 8
        
        # Pad value to 40 bits on the right
        value <<= (40 - bits)
        
        # Extract 8 5-bit groups (even if some are padding zeros)
        for j in range(8):
            if j * 5 < bits:
                # Extract 5 bits
                index = (value >> (35 - j * 5)) & 0x1F
                result.append(ALPHABET[index])
            else:
                # This is padding
                result.append(PADDING_CHAR)
    
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
        raise TypeError("input must be a str")
    
    # Check length is multiple of 8
    if len(s) % 8 != 0:
        raise ValueError("input length must be a multiple of 8")
    
    # Convert to uppercase for processing
    s_upper = s.upper()
    
    # Count and validate padding
    padding_count = 0
    for i in range(len(s_upper) - 1, -1, -1):
        if s_upper[i] == PADDING_CHAR:
            padding_count += 1
        else:
            break
    
    # Validate padding count
    if padding_count not in VALID_PADDING_COUNTS:
        raise ValueError(f"invalid padding count: {padding_count}")
    
    # Check that padding only appears at the end
    if padding_count > 0:
        # All padding should be at the end
        for i in range(len(s_upper) - padding_count):
            if s_upper[i] == PADDING_CHAR:
                raise ValueError("padding character found in non-padding position")
    
    # Validate all non-padding characters are in alphabet
    for i in range(len(s_upper) - padding_count):
        if s_upper[i] not in ALPHABET:
            raise ValueError(f"invalid character in input: {s[i]}")
    
    if len(s_upper) == 0:
        return b""
    
    result = []
    
    # Process input in groups of 8 characters
    for i in range(0, len(s_upper), 8):
        chunk = s_upper[i:i+8]
        
        # Convert characters to 5-bit values
        value = 0
        for j, char in enumerate(chunk):
            if char == PADDING_CHAR:
                # Padding bits are 0
                value = (value << 5) | 0
            else:
                index = ALPHABET.index(char)
                value = (value << 5) | index
        
        # Determine how many bytes to extract
        # Based on padding count
        if padding_count == 0:
            # 8 characters = 40 bits = 5 bytes
            num_bytes = 5
        elif padding_count == 1:
            # 7 characters + 1 padding = 35 bits = 4 bytes (32 bits used)
            num_bytes = 4
        elif padding_count == 3:
            # 5 characters + 3 padding = 25 bits = 3 bytes (24 bits used)
            num_bytes = 3
        elif padding_count == 4:
            # 4 characters + 4 padding = 20 bits = 2 bytes (16 bits used)
            num_bytes = 2
        elif padding_count == 6:
            # 2 characters + 6 padding = 10 bits = 1 byte (8 bits used)
            num_bytes = 1
        else:
            num_bytes = 0
        
        # Extract bytes from the value
        # The value has 40 bits, we need to extract the top num_bytes*8 bits
        shift = 40 - (num_bytes * 8)
        for j in range(num_bytes):
            byte_val = (value >> (shift - j * 8)) & 0xFF
            result.append(byte_val)
    
    return bytes(result)
