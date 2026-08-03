"""Utilities for computing the longest common subsequence of strings."""


def lcs_length(s1: str, s2: str) -> int:
    """Return the length of the longest common subsequence of two strings.

    Raises:
        TypeError: If either argument is not a string.
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("s1 and s2 must be strings")

    if not s1 or not s2:
        return 0
    if s1 == s2:
        return len(s1)

    # Use the shorter string for the DP row to minimize memory usage.
    if len(s1) < len(s2):
        shorter, longer = s1, s2
    else:
        shorter, longer = s2, s1

    previous = [0] * (len(shorter) + 1)

    for long_char in longer:
        current = [0]
        for index, short_char in enumerate(shorter, start=1):
            if long_char == short_char:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(previous[index], current[index - 1]))
        previous = current

    return previous[-1]
