from __future__ import annotations


def quicksort(lst: list[int]) -> list[int]:
    if len(lst) <= 1:
        return list(lst)
    pivot = lst[len(lst) // 2]
    left = [x for x in lst if x < pivot]
    middle = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]
    return quicksort(left) + middle + quicksort(right)
