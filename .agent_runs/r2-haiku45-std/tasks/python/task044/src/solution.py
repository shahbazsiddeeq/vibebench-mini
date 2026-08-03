def to_snake(s):
    """Convert camelCase to snake_case.
    
    Handles acronyms by keeping consecutive uppercase letters together,
    only splitting off the final capital that starts a new lowercased word.
    Result is fully lowercase.
    """
    if not s:
        return s
    
    result = []
    i = 0
    
    while i < len(s):
        if s[i].isupper():
            # Check if this is part of an acronym (multiple consecutive uppercase letters)
            j = i
            while j < len(s) and s[j].isupper():
                j += 1
            
            # If we have multiple uppercase letters
            if j - i > 1:
                # Check if there's a lowercase letter after the uppercase run
                if j < len(s) and s[j].islower():
                    # The last uppercase letter starts a new word
                    # Add all but the last uppercase letter as an acronym
                    if result:
                        result.append('_')
                    result.append(s[i:j-1].lower())
                    result.append('_')
                    result.append(s[j-1].lower())
                    i = j
                else:
                    # All uppercase letters at the end or followed by non-letter
                    if result:
                        result.append('_')
                    result.append(s[i:j].lower())
                    i = j
            else:
                # Single uppercase letter
                if result:
                    result.append('_')
                result.append(s[i].lower())
                i += 1
        else:
            result.append(s[i])
            i += 1
    
    return ''.join(result)


def to_camel(s):
    """Convert snake_case to camelCase.
    
    Lowercases the first letter of output and capitalizes the first letter
    of every subsequent underscore-separated part.
    """
    if not s:
        return s
    
    parts = s.split('_')
    
    # First part is lowercased
    result = [parts[0].lower()]
    
    # Subsequent parts are capitalized
    for part in parts[1:]:
        if part:  # Handle empty parts from consecutive underscores
            result.append(part[0].upper() + part[1:].lower())
    
    return ''.join(result)
