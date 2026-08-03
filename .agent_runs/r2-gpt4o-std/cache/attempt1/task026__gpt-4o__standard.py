# src/solution.py

from itertools import permutations as it_permutations

def permutations(lst):
    if len(lst) > 8:
        raise ValueError("List length exceeds 8")
    return sorted(it_permutations(lst))
