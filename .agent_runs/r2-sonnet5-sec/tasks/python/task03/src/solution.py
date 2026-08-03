"""
Palindrome Check module.

Provides is_palindrome(s) which determines whether a given string is a
palindrome after filtering to only ASCII alphanumeric characters and
lowercasing them. Non-ASCII characters, spaces, and punctuation are ignored.
"""

from typing import Any


def is_palindrome(s: Any) -> bool:
    """
    Return True if `s` reads the same forwards and backwards after
    keeping only ASCII alphanumeric characters ([A-Za-z0-9]) and
    lowercasing them. All other characters are ignored.

    Args:
        s: The input value to check. Expected to be a string.

    Returns:
        bool: True if the filtered string is a palindrome (including
              the empty string case), False otherwise.

    Raises:
        TypeError: If `s` is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    # Keep only ASCII alphanumeric characters, lowercased.
    # Using ord() check to ensure strict ASCII range filtering,
    # avoiding reliance on str.isalnum() which accepts non-ASCII
    # alphanumeric characters (e.g., accented letters, other scripts).
    filtered_chars = []
    for ch in s:
        code = ord(ch)
        if 0 <= code <= 127 and ch.isalnum():
            filtered_chars.append(ch.lower())

    filtered = "".join(filtered_chars)
    return filtered == filtered[::-1]
