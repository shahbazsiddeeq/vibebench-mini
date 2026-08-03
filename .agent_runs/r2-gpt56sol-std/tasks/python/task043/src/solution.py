def edit_distance(s1: str, s2: str) -> int:
    """Return the Levenshtein distance between two strings."""
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("edit_distance arguments must be strings")

    if len(s1) < len(s2):
        s1, s2 = s2, s1

    previous = list(range(len(s2) + 1))

    for i, char1 in enumerate(s1, start=1):
        current = [i]
        for j, char2 in enumerate(s2, start=1):
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            replacement = previous[j - 1] + (char1 != char2)
            current.append(min(insertion, deletion, replacement))
        previous = current

    return previous[-1]
