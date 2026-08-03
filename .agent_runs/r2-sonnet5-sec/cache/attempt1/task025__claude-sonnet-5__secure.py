"""
src/solution.py

A small, security-conscious implementation of a list rotation utility.

The public function `rotate(lst, k)` returns a *new* list that is the
input list rotated to the right by `k` positions. `k` may be negative
(which rotates left) or larger in magnitude than the length of the
list; both cases are handled via modular arithmetic.

Design notes / security considerations:
    * Inputs are validated strictly (no implicit, surprising coercions).
    * No use of eval/exec or other dynamic code execution.
    * No randomness is required for this task, so the `secrets` module
      is not used here, but the module avoids `random` entirely to
      keep the codebase consistent with security-first practices.
    * The original list is never mutated; a new list is always
      returned.
    * Errors are raised using standard, well-defined exception types
      with clear (but not internally revealing) messages -- no stack
      traces or internal state are leaked to callers.
"""

from typing import List, Sequence, TypeVar, Any

T = TypeVar("T")


def _validate_inputs(lst: Any, k: Any) -> None:
    """Validate the inputs to `rotate`.

    Raises:
        TypeError: if `lst` is not a list/sequence or `k` is not an int.
    """
    if isinstance(lst, (str, bytes, bytearray)):
        # Strings/bytes are sequences too, but rotating them as a
        # "list" is likely not intended; reject to avoid ambiguous
        # behavior and potential misuse.
        raise TypeError("lst must be a list, not a string/bytes type")

    if not isinstance(lst, Sequence):
        raise TypeError("lst must be a list or sequence")

    if not isinstance(lst, list):
        # Be strict: only accept actual list instances for the
        # public API to keep behavior predictable and avoid
        # accidental misuse with exotic sequence types.
        raise TypeError("lst must be a list")

    if isinstance(k, bool) or not isinstance(k, int):
        # bool is a subclass of int in Python; explicitly reject it
        # to avoid confusing True/False being treated as 1/0.
        raise TypeError("k must be an integer")


def rotate(lst: List[T], k: int) -> List[T]:
    """Return a new list rotated to the right by `k` positions.

    Args:
        lst: The list to rotate. The original list is not modified.
        k: Number of positions to rotate right. May be negative
           (rotates left) or larger than len(lst) (wraps around).

    Returns:
        A new list with the rotation applied.

    Raises:
        TypeError: if `lst` is not a list or `k` is not an integer.
    """
    _validate_inputs(lst, k)

    n = len(lst)
    if n == 0:
        return []

    effective_k = k % n  # handles negative and oversized k safely

    if effective_k == 0:
        return list(lst)

    return lst[-effective_k:] + lst[:-effective_k]
