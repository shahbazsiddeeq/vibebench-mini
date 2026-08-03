"""
src/solution.py

Implementation of the Boyer-Moore majority vote algorithm.

The module exposes a single public function, ``majority_element``, which
finds the value in a list of integers that occurs strictly more than
``len(nums) // 2`` times. The implementation is careful to validate its
inputs and never leaks internal state or stack traces to the caller;
only well-defined ``ValueError`` or ``TypeError`` exceptions with safe,
generic messages are raised.
"""

from typing import List


def majority_element(nums: List[int]) -> int:
    """
    Return the strict majority element of ``nums`` using the Boyer-Moore
    voting algorithm, followed by a verification pass.

    A strict majority element is one that appears strictly more than
    ``len(nums) // 2`` times in the list.

    Args:
        nums: A list of integers.

    Returns:
        The integer value that is the strict majority element.

    Raises:
        ValueError: If ``nums`` is empty, is not a list, contains
            non-integer elements, or if no strict majority element
            exists.
    """
    # --- Input validation -------------------------------------------------
    if not isinstance(nums, list):
        raise ValueError("Invalid input: 'nums' must be a list.")

    if len(nums) == 0:
        raise ValueError("Invalid input: 'nums' must not be empty.")

    for item in nums:
        # Explicitly reject bool as it's a subclass of int but semantically
        # different; also reject any non-int type to keep behavior strict
        # and predictable.
        if isinstance(item, bool) or not isinstance(item, int):
            raise ValueError("Invalid input: all elements must be integers.")

    # --- Boyer-Moore voting phase ------------------------------------------
    candidate = None
    count = 0

    for value in nums:
        if count == 0:
            candidate = value
            count = 1
        elif value == candidate:
            count += 1
        else:
            count -= 1

    # --- Verification phase -------------------------------------------------
    occurrences = 0
    for value in nums:
        if value == candidate:
            occurrences += 1

    if occurrences > len(nums) // 2:
        return candidate

    raise ValueError("No strict majority element exists in the given list.")
