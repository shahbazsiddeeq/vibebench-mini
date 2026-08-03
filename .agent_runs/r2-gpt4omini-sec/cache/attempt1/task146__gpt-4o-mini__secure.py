# src/solution.py

def wildcard_match(pattern: str, text: str) -> bool:
    # Validate inputs
    if not isinstance(pattern, str) or not isinstance(text, str):
        return False

    # Initialize pointers for pattern and text
    p_len = len(pattern)
    t_len = len(text)
    
    # Pointers for pattern and text
    p_idx, t_idx = 0, 0
    
    # Variables to track the last position of '*' in pattern and text
    star_idx = -1
    match_idx = 0
    
    while t_idx < t_len:
        if p_idx < p_len and (pattern[p_idx] == text[t_idx] or pattern[p_idx] == '?'):
            # Characters match or pattern has '?'
            p_idx += 1
            t_idx += 1
        elif p_idx < p_len and pattern[p_idx] == '*':
            # Found a '*', record its position
            star_idx = p_idx
            match_idx = t_idx
            p_idx += 1
        elif star_idx != -1:
            # Last pattern was '*', try to match more characters in text
            p_idx = star_idx + 1
            t_idx = match_idx + 1
            match_idx += 1
        else:
            # No match found
            return False

    # Check for remaining characters in pattern
    while p_idx < p_len and pattern[p_idx] == '*':
        p_idx += 1

    # If we have processed the entire pattern, it's a match
    return p_idx == p_len
