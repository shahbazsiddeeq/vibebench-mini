"""
src/solution.py

Longest Common Subsequence (LCS) length calculator.

This module exposes a single function, `lcs_length`, which computes the
length of the longest common subsequence between two strings using
standard dynamic programming. The implementation avoids any use of
`eval`/`exec`, performs no file or network I/O, and validates all inputs
strictly to guard against misuse or unexpected types.
"""

from typing import List


def lcs_length(s1: str, s2: str) -> int:
    """
    Compute the length of the longest common subsequence (LCS) of two strings.

    Args:
        s1: The first input string.
        s2: The second input string.

    Returns:
        The length of the longest common subsequence as a non-negative integer.

    Raises:
        TypeError: If either argument is not a string.
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Both s1 and s2 must be strings.")

    n, m = len(s1), len(s2)

    if n == 0 or m == 0:
        return 0

    # Use a rolling 2-row DP table to keep memory usage low (O(min(n, m))).
    # Ensure s2 is the shorter string for the inner loop to minimize memory.
    if m > n:
        s1, s2 = s2, s1
        n, m = m, n

    previous: List[int] = [0] * (m + 1)
    current: List[int] = [0] * (m + 1)

    for i in range(1, n + 1):
        char1 = s1[i - 1]
        for j in range(1, m + 1):
            if char1 == s2[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous, current = current, previous

    return previous[m]
