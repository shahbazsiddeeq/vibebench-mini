"""Utilities for checking palindromes."""


def is_palindrome(s: str) -> bool:
    """Return whether *s* is an ASCII-alphanumeric palindrome.

    Non-ASCII and non-alphanumeric characters are ignored, and ASCII letters
    are compared case-insensitively.
    """
    if not isinstance(s, str):
        raise TypeError("s must be a string")

    filtered = "".join(
        char.lower()
        for char in s
        if ("a" <= char <= "z")
        or ("A" <= char <= "Z")
        or ("0" <= char <= "9")
    )
    return filtered == filtered[::-1]
