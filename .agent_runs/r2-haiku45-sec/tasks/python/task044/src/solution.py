import re


def to_snake(s: str) -> str:
    """
    Convert camelCase to snake_case.
    
    Handles acronyms by keeping consecutive uppercase letters together,
    only splitting off the final capital that starts a new lowercased word.
    Result is fully lowercase.
    
    Examples:
        "myVariableName" -> "my_variable_name"
        "parseHTML" -> "parse_html"
        "HTMLParser" -> "html_parser"
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    if not s:
        return s
    
    result = []
    
    for i, char in enumerate(s):
        if char.isupper():
            # Check if this is part of an acronym (multiple consecutive uppercase)
            # or the start of a new word after lowercase letters
            if i > 0:
                prev_char = s[i - 1]
                next_char = s[i + 1] if i + 1 < len(s) else None
                
                # Add underscore if:
                # 1. Previous character is lowercase, OR
                # 2. Previous character is uppercase AND next character is lowercase
                #    (this handles the transition from acronym to new word)
                if prev_char.islower() or (prev_char.isupper() and next_char and next_char.islower()):
                    result.append('_')
            
            result.append(char.lower())
        else:
            result.append(char)
    
    return ''.join(result)


def to_camel(s: str) -> str:
    """
    Convert snake_case to camelCase.
    
    Lowercases the first letter of output and capitalizes the first letter
    of every subsequent underscore-separated part.
    
    Examples:
        "my_variable_name" -> "myVariableName"
        "my_var" -> "myVar"
        "hello" -> "hello"
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    if not s:
        return s
    
    # Split by underscore
    parts = s.split('_')
    
    if not parts:
        return s
    
    # First part: lowercase the first character
    result = [parts[0][0].lower() + parts[0][1:] if parts[0] else '']
    
    # Subsequent parts: capitalize first character, keep rest as-is
    for part in parts[1:]:
        if part:
            result.append(part[0].upper() + part[1:])
        else:
            result.append(part)
    
    return ''.join(result)
