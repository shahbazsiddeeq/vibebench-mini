from itertools import combinations
from typing import Any, Iterable


def power_set(elements: Iterable[Any]) -> list[frozenset[Any]]:
    """Return all distinct subsets, ordered by size and string representation."""
    unique_elements = list(dict.fromkeys(elements))
    subsets = [
        frozenset(combination)
        for size in range(len(unique_elements) + 1)
        for combination in combinations(unique_elements, size)
    ]
    return sorted(
        subsets,
        key=lambda subset: (
            len(subset),
            sorted(str(element) for element in subset),
        ),
    )
