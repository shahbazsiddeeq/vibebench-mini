from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from typing import List, Tuple, Any


def find_anagram_pairs(words: Any) -> List[Tuple[str, str]]:
    """
    Find all unique pairs of distinct words (by value) from `words` that are
    anagrams of each other (case-sensitive comparison).

    Args:
        words: An iterable (expected list) of strings.

    Returns:
        A sorted list of (a, b) tuples where a < b lexicographically and
        a, b are anagrams of each other.

    Raises:
        TypeError: If `words` is not a list/iterable of strings.
    """
    if not isinstance(words, (list, tuple)):
        raise TypeError("words must be a list or tuple of strings")

    validated_words: List[str] = []
    for item in words:
        if not isinstance(item, str):
            raise TypeError("all elements of words must be strings")
        validated_words.append(item)

    # Group distinct words by their sorted-character signature.
    groups: dict[Tuple[str, ...], set[str]] = defaultdict(set)
    for word in validated_words:
        key = tuple(sorted(word))
        groups[key].add(word)

    pairs: List[Tuple[str, str]] = []
    for distinct_words in groups.values():
        if len(distinct_words) < 2:
            continue
        for a, b in combinations(sorted(distinct_words), 2):
            pairs.append((a, b))

    pairs.sort()
    return pairs
