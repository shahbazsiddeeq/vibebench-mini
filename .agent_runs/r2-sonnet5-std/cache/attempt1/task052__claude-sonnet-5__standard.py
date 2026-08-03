from itertools import combinations
from collections import defaultdict


def find_anagram_pairs(words):
    groups = defaultdict(set)
    for w in words:
        groups[tuple(sorted(w))].add(w)

    pairs = set()
    for group in groups.values():
        if len(group) > 1:
            for a, b in combinations(sorted(group), 2):
                pairs.add((a, b))

    return sorted(pairs)
