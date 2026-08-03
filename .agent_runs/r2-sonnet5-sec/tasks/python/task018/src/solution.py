"""
src/solution.py

A secure, self-contained implementation of iterative binary search.

Design notes (security-focused):
    - Strict input validation: only accepts list/tuple-like sequences
      (supporting __len__ and __getitem__), rejects non-sequence types.
    - No use of eval/exec or any dynamic code execution.
    - No external/untrusted data parsing, no I/O.
    - No randomness needed for this task, so `secrets` is not used here,
      but if random values were ever required, `secrets` would be the
      module of choice for cryptographic-quality randomness.
    - Defensive error handling: raises clear, non-leaky exceptions
      (no internal state or stack traces exposed) on invalid input,
      rather than letting an unrelated exception propagate.
    - Avoids mutating the input sequence.
    - Uses only integer arithmetic for index computation to avoid
      overflow-related issues (not a concern in Python, but done for
      correctness/clarity).
"""

from typing import Sequence, Any


def _validate_arr(arr: Any) -> None:
    """
    Validate that `arr` is a proper sequence type suitable for
    binary search (supports indexing and length).

    Raises:
        TypeError: if arr is not a valid sequence (list/tuple or
                    similar sequence supporting __len__/__getitem__).
    """
    if arr is None:
        raise TypeError("arr must not be None")

    # Explicitly reject strings/bytes/mappings which are technically
    # sequences but not appropriate here (also guards against subtle
    # misuse where a string is passed where a list of items is expected).
    if isinstance(arr, (str, bytes, bytearray, dict, set, frozenset)):
        raise TypeError("arr must be a list or tuple of comparable elements")

    if not hasattr(arr, "__len__") or not hasattr(arr, "__getitem__"):
        raise TypeError("arr must be a sequence supporting len() and indexing")


def binary_search(arr: Sequence[Any], target: Any) -> int:
    """
    Perform an iterative binary search on a sorted sequence `arr`
    to find `target`.

    Args:
        arr: A sorted sequence (list or tuple) of comparable elements,
             in ascending order.
        target: The value to search for. Must be comparable to the
                elements of `arr`.

    Returns:
        The index of `target` in `arr` if found, otherwise -1.

    Raises:
        TypeError: If `arr` is not a valid sequence type or if
                   `target` is not comparable to the elements of `arr`.
    """
    _validate_arr(arr)

    n = len(arr)
    low = 0
    high = n - 1

    while low <= high:
        mid = low + (high - low) // 2

        try:
            mid_val = arr[mid]
        except (IndexError, KeyError) as exc:
            # Should not happen given valid bounds, but guard defensively
            # without leaking internal details.
            raise TypeError("arr does not support required indexing") from exc

        try:
            if mid_val == target:
                return mid
            elif mid_val < target:
                low = mid + 1
            else:
                high = mid - 1
        except TypeError as exc:
            # Comparison failed (e.g., incompatible types) - surface a
            # clear, sanitized error without exposing internal details.
            raise TypeError("target is not comparable to elements of arr") from exc

    return -1
