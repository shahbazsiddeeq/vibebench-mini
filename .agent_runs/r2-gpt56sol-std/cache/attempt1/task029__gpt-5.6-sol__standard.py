"""Longest common subsequence utilities."""


def lcs_length(s1: str, s2: str) -> int:
    """Return the length of the longest common subsequence of two strings."""
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    previous = [0] * (len(s2) + 1)

    for char1 in s1:
        current = [0]
        for index, char2 in enumerate(s2, start=1):
            if char1 == char2:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(previous[index], current[-1]))
        previous = current

    return previous[-1]
