"""Generate all positional permutations in ascending order."""

from itertools import permutations as _itertools_permutations
from typing import Any


def permutations(lst: list[Any]) -> list[tuple[Any, ...]]:
    """Return all positional permutations of *lst*, sorted ascending.

    Duplicate values remain duplicated because permutations are based on
    positions. At most eight elements are accepted.
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if len(lst) > 8:
        raise ValueError("lst must contain at most 8 elements")

    return sorted(_itertools_permutations(lst))
