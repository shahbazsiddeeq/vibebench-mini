from collections import defaultdict
from itertools import combinations
from typing import Iterable


def find_anagram_pairs(words: Iterable[str]) -> list[tuple[str, str]]:
    """Return sorted unique pairs of distinct, case-sensitive anagrams."""
    groups: dict[str, set[str]] = defaultdict(set)

    for word in words:
        groups["".join(sorted(word))].add(word)

    pairs = [
        pair
        for group in groups.values()
        for pair in combinations(sorted(group), 2)
    ]
    return sorted(pairs)
