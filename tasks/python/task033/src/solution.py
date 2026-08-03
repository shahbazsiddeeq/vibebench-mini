from __future__ import annotations

from collections import defaultdict


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[tuple, list[str]] = defaultdict(list)
    for w in words:
        key = tuple(sorted(w))
        groups[key].append(w)
    result = [sorted(g) for g in groups.values()]
    return sorted(result, key=lambda g: g[0])
