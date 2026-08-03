"""Utilities for counting unique characters."""

from collections import Counter


def unique_char_count(s: str) -> dict[str, int]:
    """Return characters occurring exactly once, in first-appearance order."""
    if not isinstance(s, str):
        raise TypeError("s must be a string")

    counts = Counter(s)
    return {character: 1 for character in s if counts[character] == 1}
