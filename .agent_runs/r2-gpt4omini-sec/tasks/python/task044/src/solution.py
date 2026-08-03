# src/solution.py

def to_snake(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    
    result = []
    previous_char = ''
    
    for char in s:
        if char.isupper():
            if previous_char and previous_char.islower():
                result.append('_')
            elif previous_char and previous_char.isupper():
                if result and result[-1] != '_':
                    result.append('_')
            result.append(char.lower())
        else:
            result.append(char)
        previous_char = char
    
    return ''.join(result)

def to_camel(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    
    parts = s.split('_')
    if not parts:
        return ''
    
    return parts[0].lower() + ''.join(part.capitalize() for part in parts[1:])
