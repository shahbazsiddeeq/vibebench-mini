def to_snake(s):
    if not s:
        return s
    
    result = []
    for i, char in enumerate(s):
        if char.isupper():
            # Add underscore if:
            # 1. Not at start AND
            # 2. Either previous char is lowercase OR next char is lowercase (and current is start of new word)
            if i > 0:
                prev_is_lower = s[i-1].islower()
                next_is_lower = i + 1 < len(s) and s[i+1].islower()
                
                # Insert underscore if previous is lowercase (start of capital sequence)
                # OR if next is lowercase and previous is uppercase (end of acronym, start of new word)
                if prev_is_lower or (next_is_lower and s[i-1].isupper()):
                    result.append('_')
            
            result.append(char.lower())
        else:
            result.append(char)
    
    return ''.join(result)


def to_camel(s):
    if not s:
        return s
    
    parts = s.split('_')
    if not parts:
        return s
    
    # First part: lowercase
    result = [parts[0].lower()]
    
    # Remaining parts: capitalize first letter
    for part in parts[1:]:
        if part:  # Skip empty parts
            result.append(part[0].upper() + part[1:].lower() if len(part) > 1 else part.upper())
    
    return ''.join(result)
