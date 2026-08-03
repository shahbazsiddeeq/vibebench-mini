# src/solution.py

import re
from secrets import choice

def rle_encode(s: str) -> str:
    if any(char.isdigit() for char in s):
        raise ValueError("Input contains digits, which are not allowed.")
    
    if not s:
        return ""
    
    encoded = []
    current_char = s[0]
    count = 1
    
    for char in s[1:]:
        if char == current_char:
            count += 1
        else:
            encoded.append(f"{count}{current_char}")
            current_char = char
            count = 1
    
    encoded.append(f"{count}{current_char}")
    return ''.join(encoded)

def rle_decode(s: str) -> str:
    if not s:
        return ""
    
    if not re.fullmatch(r'(\d+[^\d])+', s):
        raise ValueError("Malformed input.")
    
    decoded = []
    matches = re.finditer(r'(\d+)([^\d])', s)
    
    for match in matches:
        count = int(match.group(1))
        char = match.group(2)
        decoded.append(char * count)
    
    return ''.join(decoded)
