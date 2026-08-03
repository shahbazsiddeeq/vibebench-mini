"""Utilities for finding anagram pairs."""

from collections.abc import Iterable


def find_anagram_pairs(words: Iterable[str]) -> list[tuple[str, str]]:
    """Return sorted, unique pairs of distinct case-sensitive anagrams.

    Args:
        words: An iterable containing only strings.

    Raises:
        TypeError: If ``words`` is not an iterable of strings.
    """
    if isinstance(words, (str, bytes)) or not isinstance(words, Iterable):
        raise TypeError("words must be an iterable of strings")

    groups: dict[tuple[str, ...], set[str]] = {}

    for word in words:
        if not isinstance(word, str):
            raise TypeError("all words must be strings")
        signature = tuple(sorted(word))
        groups.setdefault(signature, set()).add(word)

    pairs: list[tuple[str, str]] = []
    for group in groups.values():
        unique_words = sorted(group)
        for index, first in enumerate(unique_words):
            for second in unique_words[index + 1:]:
                pairs.append((first, second))

    pairs.sort()
    return pairs
