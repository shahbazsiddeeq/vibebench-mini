from __future__ import annotations


def rotate(lst: list, k: int) -> list:
    if not lst:
        return []
    n = len(lst)
    k = k % n
    return lst[-k:] + lst[:-k] if k else lst[:]
