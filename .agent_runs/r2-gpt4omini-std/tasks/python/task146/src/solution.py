def wildcard_match(pattern: str, text: str) -> bool:
    # Initialize pointers for pattern and text
    p_len, t_len = len(pattern), len(text)
    p_idx, t_idx = 0, 0
    star_idx, match_idx = -1, -1

    while t_idx < t_len:
        # If characters match or pattern has '?', move both pointers
        if p_idx < p_len and (pattern[p_idx] == text[t_idx] or pattern[p_idx] == '?'):
            p_idx += 1
            t_idx += 1
        # If pattern has '*', record the position and move the pattern pointer
        elif p_idx < p_len and pattern[p_idx] == '*':
            star_idx = p_idx
            match_idx = t_idx
            p_idx += 1
        # If last pattern was '*', try to match the next character in text
        elif star_idx != -1:
            p_idx = star_idx + 1
            t_idx = match_idx + 1
            match_idx += 1
        else:
            return False

    # Check for remaining characters in pattern
    while p_idx < p_len and pattern[p_idx] == '*':
        p_idx += 1

    return p_idx == p_len
