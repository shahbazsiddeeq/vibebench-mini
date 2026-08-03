"""Utilities for finding frequent words in text."""

from collections import Counter


def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """Return the k most frequent case-insensitive alphanumeric words.

    Words are contiguous sequences of Unicode alphanumeric characters.
    Results are ordered by descending frequency, with lexicographic ordering
    used to break ties.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer")
    if k <= 0 or not text:
        return []

    words: list[str] = []
    current: list[str] = []

    for character in text:
        if character.isalnum():
            current.append(character)
        elif current:
            words.append("".join(current).casefold())
            current.clear()

    if current:
        words.append("".join(current).casefold())

    counts = Counter(words)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]
