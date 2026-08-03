"""
Kth Largest element finder using the Quickselect algorithm.

This module exposes a single public function, ``kth_largest``, that
returns the k-th largest value from a list of integers. It uses the
quickselect algorithm for average O(n) performance and relies on the
``secrets`` module (rather than the ``random`` module) for choosing
pivot indices, to avoid using a predictable/non-cryptographic PRNG
anywhere in the code path -- even though pivot selection here has no
security sensitivity, this keeps the module consistent with a
security-conscious coding standard and avoids any dependency on
``random``.

The function performs strict input validation:
  * ``nums`` must be a list (not a generic iterable, str, etc.).
  * every element of ``nums`` must be an ``int`` (bool is rejected,
    since bool is a subclass of int and is not a meaningful "number"
    in this context).
  * ``nums`` must be non-empty.
  * ``k`` must be an ``int`` in the inclusive range ``1..len(nums)``.

On invalid input, a ``ValueError`` is raised with a generic message
that does not leak internal implementation details.
"""

from __future__ import annotations

import secrets
from typing import List


__all__ = ["kth_largest"]


def _validate_inputs(nums: List[int], k: int) -> None:
    """Validate inputs for kth_largest, raising ValueError on failure."""
    if not isinstance(nums, list):
        raise ValueError("nums must be a list of integers")

    if len(nums) == 0:
        raise ValueError("nums must not be empty")

    for item in nums:
        # Reject bool explicitly since bool is a subclass of int.
        if isinstance(item, bool) or not isinstance(item, int):
            raise ValueError("nums must contain only integers")

    if isinstance(k, bool) or not isinstance(k, int):
        raise ValueError("k must be an integer")

    if k < 1 or k > len(nums):
        raise ValueError("k must be in the range 1..len(nums)")


def kth_largest(nums: List[int], k: int) -> int:
    """
    Return the k-th largest value in ``nums`` using quickselect.

    k=1 corresponds to the maximum value. Duplicates are counted by
    position, so kth_largest([3, 3, 3], 2) == 3.

    Raises:
        ValueError: if nums is empty, not a list, contains non-int
            elements, or if k is not an integer in 1..len(nums).
    """
    _validate_inputs(nums, k)

    # Work on a copy to avoid mutating the caller's list.
    arr = list(nums)
    n = len(arr)

    # Convert "k-th largest" into a 0-indexed target position for the
    # equivalent "k-th smallest in descending order" problem. If we
    # sort in ascending order, the k-th largest sits at index n - k.
    target_index = n - k

    lo, hi = 0, n - 1
    while True:
        if lo == hi:
            return arr[lo]

        pivot_index = _partition(arr, lo, hi)

        if pivot_index == target_index:
            return arr[pivot_index]
        elif pivot_index < target_index:
            lo = pivot_index + 1
        else:
            hi = pivot_index - 1


def _partition(arr: List[int], lo: int, hi: int) -> int:
    """
    Partition arr[lo..hi] (inclusive) around a randomly chosen pivot,
    using the Lomuto partition scheme. Returns the final index of the
    pivot after partitioning, with all elements <= pivot to its left
    and all elements > pivot to its right (ascending order semantics).
    """
    # Choose a random pivot index using a CSPRNG-backed source to
    # avoid worst-case adversarial inputs and to sidestep use of the
    # non-cryptographic 'random' module.
    pivot_choice = lo + secrets.randbelow(hi - lo + 1)
    arr[pivot_choice], arr[hi] = arr[hi], arr[pivot_choice]
    pivot_value = arr[hi]

    store_index = lo
    for i in range(lo, hi):
        if arr[i] < pivot_value:
            arr[i], arr[store_index] = arr[store_index], arr[i]
            store_index += 1

    arr[store_index], arr[hi] = arr[hi], arr[store_index]
    return store_index
