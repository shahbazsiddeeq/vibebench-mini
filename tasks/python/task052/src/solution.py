from __future__ import annotations


def find_anagram_pairs(words: list[str]) -> list[tuple[str, str]]:
    pairs = []
    n = len(words)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = words[i], words[j]
            if a != b and sorted(a) == sorted(b):
                pair = (a, b) if a < b else (b, a)
                if pair not in pairs:
                    pairs.append(pair)
    return sorted(pairs)
