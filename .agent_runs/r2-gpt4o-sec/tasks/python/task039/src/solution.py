import re
from secrets import choice
from string import ascii_letters, punctuation, whitespace

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
    tokens = re.findall(r'(\d+)([^\d])', s)
    
    for count, char in tokens:
        if count == '0':
            raise ValueError("Count cannot be zero.")
        decoded.append(char * int(count))
    
    return ''.join(decoded)
