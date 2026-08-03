# src/solution.py

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
    
    decoded = []
    count = 0
    
    for char in s:
        if char.isdigit():
            count = count * 10 + int(char)
        else:
            if count == 0:
                raise ValueError("Malformed input: no count before character.")
            decoded.append(char * count)
            count = 0
    
    if count != 0:
        raise ValueError("Malformed input: ends with a count.")
    
    return ''.join(decoded)
