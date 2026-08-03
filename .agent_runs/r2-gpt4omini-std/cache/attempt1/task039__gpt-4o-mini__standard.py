# src/solution.py

def rle_encode(s: str) -> str:
    if any(char.isdigit() for char in s):
        raise ValueError("Input must not contain ASCII digits.")
    
    if not s:
        return ""
    
    encoded = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            encoded.append(f"{count}{s[i - 1]}")
            count = 1
    
    encoded.append(f"{count}{s[-1]}")
    return ''.join(encoded)

def rle_decode(s: str) -> str:
    if not s:
        return ""
    
    decoded = []
    i = 0
    
    while i < len(s):
        count_str = ''
        
        while i < len(s) and s[i].isdigit():
            count_str += s[i]
            i += 1
        
        if not count_str or int(count_str) == 0:
            raise ValueError("Invalid input: count must be non-zero.")
        
        if i >= len(s) or not s[i].isalpha():
            raise ValueError("Invalid input: expected a character after count.")
        
        count = int(count_str)
        char = s[i]
        decoded.append(char * count)
        i += 1
    
    return ''.join(decoded)
