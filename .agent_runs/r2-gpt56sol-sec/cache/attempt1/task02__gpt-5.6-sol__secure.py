"""Utilities for reversing whitespace-separated words."""


def reverse_words(s: str) -> str:
    """Return the whitespace-separated words in *s* in reverse order."""
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    return " ".join(reversed(s.split()))
