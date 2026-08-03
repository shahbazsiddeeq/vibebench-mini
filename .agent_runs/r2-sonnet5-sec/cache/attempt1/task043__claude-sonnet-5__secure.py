"""
Levenshtein Distance implementation.

Provides a single function `edit_distance(s1, s2)` that computes the
minimum number of single-character insertions, deletions, or
substitutions required to transform s1 into s2.

This module performs strict input validation to avoid unexpected
behavior or leaking internal error details, and relies only on the
Python standard library.
"""

from typing import Any


def _validate_string(value: Any, name: str) -> str:
    """
    Validate that `value` is a string.

    Raises:
        TypeError: if value is not a str instance.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def edit_distance(s1: str, s2: str) -> int:
    """
    Compute the Levenshtein (edit) distance between two strings.

    Insertion, deletion, and substitution each cost 1.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The minimum edit distance between s1 and s2 as a non-negative int.

    Raises:
        TypeError: if s1 or s2 is not a string.
    """
    s1 = _validate_string(s1, "s1")
    s2 = _validate_string(s2, "s2")

    len1, len2 = len(s1), len(s2)

    # Handle trivial cases early.
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1

    # Use a single-row DP to keep memory usage O(min(len1, len2)).
    # Ensure s2 is the shorter string for the row dimension.
    if len2 > len1:
        s1, s2 = s2, s1
        len1, len2 = len2, len1

    previous_row = list(range(len2 + 1))

    for i in range(1, len1 + 1):
        current_row = [i] + [0] * len2
        char1 = s1[i - 1]
        for j in range(1, len2 + 1):
            char2 = s2[j - 1]
            deletion_cost = previous_row[j] + 1
            insertion_cost = current_row[j - 1] + 1
            substitution_cost = previous_row[j - 1] + (0 if char1 == char2 else 1)
            current_row[j] = min(deletion_cost, insertion_cost, substitution_cost)
        previous_row = current_row

    return previous_row[len2]
