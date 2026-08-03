# src/solution.py

def to_snake(s: str) -> str:
    result = []
    prev_char = ''
    
    for char in s:
        if char.isupper():
            if result and prev_char.islower():
                result.append('_')
            result.append(char.lower())
        else:
            result.append(char)
        prev_char = char
    
    return ''.join(result)

def to_camel(s: str) -> str:
    parts = s.split('_')
    return parts[0].lower() + ''.join(part.capitalize() for part in parts[1:])
