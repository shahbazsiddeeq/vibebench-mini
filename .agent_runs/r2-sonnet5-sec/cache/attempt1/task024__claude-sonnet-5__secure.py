"""
src/solution.py

Provides `count_occurrences`, a helper that counts how many times a target
value appears in a sorted sequence using binary search (O(log n) comparisons).

Design notes / security considerations:
- No use of eval/exec or any dynamic code execution.
- No external randomness needed; if randomness were required, `secrets`
  would be used instead of `random`.
- Input is validated defensively: we only require that `arr` behaves like a
  sequence (supports `len()` and integer indexing) so that both plain lists
  and custom sequence-like objects (e.g., test doubles that track access
  counts) work correctly.
- We avoid leaking internal implementation details or stack traces to the
  caller; invalid input results in a clean `TypeError`/`ValueError` with a
  generic, non-sensitive message.
- No I/O, no printing, no logging of user data.
"""

from typing import Any, Sequence


def _validate_sequence(arr: Any) -> None:
    """Ensure `arr` behaves like a sequence supporting len() and indexing.

    Raises:
        TypeError: if `arr` does not support the minimal sequence protocol.
    """
    if arr is None:
        raise TypeError("arr must be a sequence, not None")

    if not hasattr(arr, "__len__") or not hasattr(arr, "__getitem__"):
        raise TypeError("arr must support len() and indexing (a sequence)")


def _bisect_left(arr: Sequence[Any], target: Any, lo: int, hi: int) -> int:
    """Return the leftmost insertion index for `target` in arr[lo:hi]."""
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _bisect_right(arr: Sequence[Any], target: Any, lo: int, hi: int) -> int:
    """Return the rightmost insertion index for `target` in arr[lo:hi]."""
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_occurrences(arr: Sequence[Any], target: Any) -> int:
    """Count how many times `target` appears in a sorted sequence `arr`.

    Uses binary search (two passes: leftmost and rightmost bounds) so that
    the number of element accesses is O(log n) rather than O(n).

    Args:
        arr: A sorted sequence (ascending order) supporting `len()` and
            indexing via `__getitem__`.
        target: The value to count occurrences of. Must be comparable to
            the elements of `arr` using `<` and `<=`.

    Returns:
        The number of times `target` occurs in `arr`.

    Raises:
        TypeError: if `arr` is not a valid sequence, or if elements are not
            comparable to `target`.
    """
    _validate_sequence(arr)

    try:
        n = len(arr)
    except Exception as exc:
        raise TypeError("arr must support len()") from exc

    if n == 0:
        return 0

    try:
        left = _bisect_left(arr, target, 0, n)
        right = _bisect_right(arr, target, 0, n)
    except TypeError as exc:
        # Comparison between target and arr elements failed (e.g. mismatched
        # types). Surface a clean, generic error without internal details.
        raise TypeError("target is not comparable with elements of arr") from exc

    return right - left
