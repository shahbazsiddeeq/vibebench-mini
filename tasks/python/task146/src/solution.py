def wildcard_match(pattern: str, text: str) -> bool:
    """Return True if pattern (with '*' and '?' wildcards) matches all of text."""
    i = 0  # index into pattern
    j = 0  # index into text
    n, m = len(pattern), len(text)
    star_p = -1  # position in pattern just after the last '*'
    star_j = 0   # position in text when the last '*' was seen
    while j < m:
        if i < n and (pattern[i] == "?" or pattern[i] == text[j]):
            i += 1
            j += 1
        elif i < n and pattern[i] == "*":
            star_p = i + 1
            star_j = j
            i = i + 1
        elif star_p != -1:
            # backtrack: let the last '*' absorb one more character
            i = star_p
            star_j += 1
            j = star_j
        else:
            return False
    # consume any trailing '*' in the pattern
    while i < n and pattern[i] == "*":
        i += 1
    return i == n
