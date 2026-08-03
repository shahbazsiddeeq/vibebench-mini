from __future__ import annotations

import itertools


def permutations(lst: list) -> list[tuple]:
    if len(lst) > 8:
        raise ValueError("input too large (max 8 elements)")
    return sorted(itertools.permutations(lst))
