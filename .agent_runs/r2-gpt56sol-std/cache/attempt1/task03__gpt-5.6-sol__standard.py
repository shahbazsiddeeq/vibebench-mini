"""Utilities for checking palindromes."""


def is_palindrome(s: str) -> bool:
    """Return whether the ASCII-alphanumeric characters in *s* form a palindrome."""
    normalized = "".join(
        char.lower()
        for char in s
        if ("a" <= char <= "z")
        or ("A" <= char <= "Z")
        or ("0" <= char <= "9")
    )
    return normalized == normalized[::-1]
