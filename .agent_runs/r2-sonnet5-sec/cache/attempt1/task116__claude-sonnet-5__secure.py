"""
Power Set Generator
--------------------

Provides `power_set(elements)` which computes the power set of a collection
of (hashable) elements, returning a list of `frozenset` objects.

Duplicate values in the input are treated as a single distinct value.
The result is sorted first by subset size (ascending), then
lexicographically by the ascending-sorted list of the string
representations of the subset's elements.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable, List


def _validate_and_normalize(elements: Any) -> List[Any]:
    """
    Validate the input and return a de-duplicated list of hashable elements.

    Raises:
        TypeError: if `elements` is not an iterable of hashable items,
                   or is a type we explicitly disallow (e.g. str/bytes/dict
                   would be ambiguous as "collections of elements").
    """
    if elements is None:
        raise TypeError("elements must be an iterable, not None")

    # Disallow strings/bytes as the top-level container to avoid ambiguous
    # semantics (iterating characters vs. treating as a single element).
    if isinstance(elements, (str, bytes, bytearray)):
        raise TypeError("elements must be a list/tuple/set of items, not a string or bytes")

    if not isinstance(elements, Iterable):
        raise TypeError("elements must be iterable")

    seen = []
    seen_set = set()
    for item in elements:
        try:
            hash(item)
        except TypeError as exc:
            raise TypeError("all elements must be hashable") from exc

        if item not in seen_set:
            seen_set.add(item)
            seen.append(item)

    return seen


def power_set(elements: Iterable[Any]) -> List[frozenset]:
    """
    Compute the power set of `elements`.

    Args:
        elements: An iterable of hashable items. Duplicates are treated
                  as a single distinct value.

    Returns:
        A list of frozensets representing every subset of the distinct
        elements, sorted first by subset size (ascending), then
        lexicographically by the ascending-sorted list of the string
        representations of the subset's elements.

    Raises:
        TypeError: if input is invalid (not iterable, or contains
                   unhashable items).
    """
    try:
        items = _validate_and_normalize(elements)
    except TypeError:
        # Re-raise with a generic, non-leaking message to avoid exposing
        # internal details, while still preserving the exception type.
        raise TypeError("Invalid input: 'elements' must be an iterable of hashable items")

    n = len(items)
    subsets: List[frozenset] = []

    for r in range(n + 1):
        for combo in combinations(items, r):
            subsets.append(frozenset(combo))

    def sort_key(s: frozenset):
        return (len(s), sorted(str(x) for x in s))

    subsets.sort(key=sort_key)
    return subsets
