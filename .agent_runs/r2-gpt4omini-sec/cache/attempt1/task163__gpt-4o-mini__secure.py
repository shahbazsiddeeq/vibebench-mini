# src/solution.py

import secrets

BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
PADDING_CHAR = '='

def base32_encode(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input must be bytes or bytearray.")
    
    output = []
    bits = 0
    value = 0
    for byte in data:
        value = (value << 8) | byte
        bits += 8
        while bits >= 5:
            bits -= 5
            output.append(BASE32_ALPHABET[(value >> bits) & 0x1F])
    
    if bits > 0:
        output.append(BASE32_ALPHABET[(value << (5 - bits)) & 0x1F])
    
    # Add padding
    padding_length = (8 - len(output) % 8) % 8
    output.extend([PADDING_CHAR] * padding_length)
    
    return ''.join(output)

def base32_decode(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    
    s = s.strip().upper()
    
    if len(s) % 8 != 0:
        raise ValueError("Input length must be a multiple of 8.")
    
    padding_count = s.count(PADDING_CHAR)
    if padding_count > 0:
        if s[-padding_count:] != PADDING_CHAR * padding_count:
            raise ValueError("Invalid padding.")
        if padding_count not in {0, 1, 3, 4, 6}:
            raise ValueError("Invalid number of padding characters.")
    
    output = bytearray()
    bits = 0
    value = 0
    
    for char in s:
        if char == PADDING_CHAR:
            continue
        if char not in BASE32_ALPHABET:
            raise ValueError(f"Invalid character '{char}' in input.")
        
        value = (value << 5) | BASE32_ALPHABET.index(char)
        bits += 5
        
        if bits >= 8:
            bits -= 8
            output.append((value >> bits) & 0xFF)
    
    return bytes(output)
