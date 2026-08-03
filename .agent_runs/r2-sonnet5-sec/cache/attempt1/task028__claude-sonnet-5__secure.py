"""
src/solution.py

A secure, self-contained implementation of the quicksort algorithm.

The public function `quicksort` sorts a list of comparable items and
returns a new sorted list, without relying on Python's built-in
`sorted()` or `list.sort()`.

Security considerations:
    - Input is strictly validated to be a list before any processing.
    - No use of eval/exec or other unsafe constructs.
    - Randomness (used only to pick a pivot, to avoid predictable
      worst-case behavior on adversarial input) is sourced from the
      `secrets` module rather than `random`.
    - Errors are raised with generic, non-revealing messages so that
      internal implementation details are not exposed to callers.
"""

from __future__ import annotations

import secrets
from typing import Any, List


def quicksort(lst: List[Any]) -> List[Any]:
    """
    Return a new sorted list containing the elements of `lst`, sorted
    in ascending order using the quicksort algorithm.

    Args:
        lst: A list of mutually comparable elements.

    Returns:
        A new list with the elements of `lst` sorted in ascending order.

    Raises:
        TypeError: If `lst` is not a list, or if its elements are not
            mutually comparable.
    """
    if not isinstance(lst, list):
        raise TypeError("quicksort expects a list as input")

    # Work on a shallow copy to avoid mutating the caller's list and to
    # avoid any aliasing issues during recursive partitioning.
    items = list(lst)
    return _quicksort(items)


def _quicksort(items: List[Any]) -> List[Any]:
    """
    Internal recursive quicksort implementation.

    Args:
        items: A list of comparable elements.

    Returns:
        A new sorted list.

    Raises:
        TypeError: If elements are not mutually comparable.
    """
    n = len(items)
    if n <= 1:
        return items

    # Choose a pivot using a cryptographically secure random index to
    # help avoid worst-case O(n^2) behavior on adversarially ordered
    # input (e.g., already-sorted or reverse-sorted lists).
    pivot_index = secrets.randbelow(n)
    pivot = items[pivot_index]

    less: List[Any] = []
    equal: List[Any] = []
    greater: List[Any] = []

    for item in items:
        try:
            if item < pivot:
                less.append(item)
            elif item > pivot:
                greater.append(item)
            else:
                equal.append(item)
        except TypeError:
            # Do not leak internal state; provide a clear, generic error.
            raise TypeError(
                "All elements of the list must be mutually comparable"
            ) from None

    return _quicksort(less) + equal + _quicksort(greater)
