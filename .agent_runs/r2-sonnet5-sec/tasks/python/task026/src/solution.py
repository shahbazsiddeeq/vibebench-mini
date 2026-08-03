"""
src/solution.py

Provides `permutations(lst)`, which returns every ordering of the
input list as a list of tuples, sorted in ascending order.

Security considerations:
- Input is strictly validated (must be a list, length bounded).
- No use of eval/exec or any dynamic code execution.
- No external randomness is required for this deterministic task,
  but if randomness were needed, the `secrets` module would be used.
- Errors are raised with generic, non-sensitive messages that do not
  leak internal state or stack details.
"""

from itertools import permutations as _itertools_permutations
from typing import Any, List, Tuple

MAX_LENGTH = 8


def permutations(lst: Any) -> List[Tuple[Any, ...]]:
    """
    Return every ordering of `lst` as a list of tuples, sorted in
    ascending order.

    Args:
        lst: A list (or list-like sequence) of elements. Length must
             be at most MAX_LENGTH (8).

    Returns:
        A list of tuples representing every permutation of `lst`,
        taken by position (duplicates in value produce duplicate
        tuples), sorted in ascending order.

    Raises:
        ValueError: If `lst` is not a list, or if its length exceeds
                    MAX_LENGTH.
    """
    if not isinstance(lst, list):
        raise ValueError("Input must be a list.")

    if len(lst) > MAX_LENGTH:
        raise ValueError(f"Input list length must not exceed {MAX_LENGTH}.")

    # itertools.permutations already generates permutations by position
    # (index-based), preserving duplicate values as distinct entries.
    all_perms = list(_itertools_permutations(lst))

    # Sort the resulting tuples in ascending order. This requires that
    # elements support ordering comparisons; if not, a TypeError will
    # naturally propagate, which is acceptable behavior here.
    all_perms.sort()

    return all_perms
