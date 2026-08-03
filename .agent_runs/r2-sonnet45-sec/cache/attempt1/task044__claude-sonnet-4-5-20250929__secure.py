def to_snake(s: str) -> str:
    """
    Convert camelCase to snake_case.
    
    Handles acronyms by keeping consecutive uppercase letters together,
    only splitting when an uppercase letter precedes a lowercase letter.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    if not s:
        return s
    
    result = []
    
    for i, char in enumerate(s):
        if char.isupper():
            # Add underscore before uppercase letter if:
            # 1. Not at the start
            # 2. Previous char is lowercase OR
            # 3. Next char is lowercase (end of acronym)
            if i > 0:
                prev_is_lower = s[i - 1].islower()
                next_is_lower = i + 1 < len(s) and s[i + 1].islower()
                
                if prev_is_lower or next_is_lower:
                    result.append('_')
            
            result.append(char.lower())
        else:
            result.append(char)
    
    return ''.join(result)


def to_camel(s: str) -> str:
    """
    Convert snake_case to camelCase.
    
    First letter is always lowercase, first letter after each underscore
    is capitalized.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    if not s:
        return s
    
    parts = s.split('_')
    
    # First part is lowercased entirely
    result = [parts[0].lower()] if parts else []
    
    # Subsequent parts have first letter capitalized
    for part in parts[1:]:
        if part:  # Skip empty parts from consecutive underscores
            result.append(part[0].upper() + part[1:].lower() if len(part) > 1 else part.upper())
    
    return ''.join(result)
