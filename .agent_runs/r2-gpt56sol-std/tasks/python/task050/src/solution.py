from collections import Counter


def unique_char_count(s: str) -> dict[str, int]:
    """Return characters occurring exactly once, in first-appearance order."""
    counts = Counter(s)
    return {char: 1 for char in s if counts[char] == 1}
