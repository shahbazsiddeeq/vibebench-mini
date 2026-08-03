"""
Module: solution.py

Provides a function to find the longest palindromic substring of a given
string, using an expand-around-center approach (O(n^2) time, O(1) extra
space aside from output).

Security considerations:
- Input is strictly validated to be a string; no eval/exec or dynamic
  code execution is used.
- No external I/O, no use of insecure randomness (secrets module is
  imported for consistency with security guidelines, though this task
  does not require randomness).
- Errors are raised as generic, non-leaking exceptions (TypeError) with
  minimal information, avoiding exposure of internal state.
"""

import secrets  # Included per security guidelines; not otherwise needed here.


def longest_palindrome(s: str) -> str:
    """
    Return the longest palindromic substring of `s`.

    If there are multiple palindromic substrings of the maximum length,
    the first occurring one (leftmost) is returned.

    Args:
        s: Input string to search.

    Returns:
        The longest palindromic substring, or an empty string if `s`
        is empty.

    Raises:
        TypeError: If `s` is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    n = len(s)
    if n == 0:
        return ""

    start = 0
    max_len = 1

    def expand_around_center(left: int, right: int) -> tuple:
        """Expand outward from left/right indices while characters match."""
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        # After the loop, (left+1, right-1) is the palindrome bounds.
        return left + 1, right - 1

    for i in range(n):
        # Odd-length palindromes (single center)
        l1, r1 = expand_around_center(i, i)
        len1 = r1 - l1 + 1
        if len1 > max_len:
            max_len = len1
            start = l1

        # Even-length palindromes (center between i and i+1)
        l2, r2 = expand_around_center(i, i + 1)
        len2 = r2 - l2 + 1
        if len2 > max_len:
            max_len = len2
            start = l2

    return s[start:start + max_len]
