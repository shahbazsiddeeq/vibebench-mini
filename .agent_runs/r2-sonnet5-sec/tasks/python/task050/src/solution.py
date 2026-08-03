"""
Module: solution.py

Provides a utility function to count characters that appear exactly once
in a given string, preserving first-appearance order.

Security considerations:
- Input is strictly validated to be a string; no eval/exec or dynamic
  code execution is used.
- No I/O, no external data sources, no randomness required.
- Errors are raised with generic, non-revealing messages to avoid
  leaking internal implementation details.
"""

from collections import Counter
from typing import Dict


def unique_char_count(s: str) -> Dict[str, int]:
    """
    Return a dict mapping each character that appears exactly once in `s`
    to the value 1. Keys are ordered by their first appearance in `s`.

    Args:
        s: The input string to analyze.

    Returns:
        A dict of {char: 1} for each character occurring exactly once,
        preserving first-appearance order.

    Raises:
        TypeError: If `s` is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    if s == "":
        return {}

    counts = Counter(s)

    result: Dict[str, int] = {}
    for ch in s:
        if counts[ch] == 1 and ch not in result:
            result[ch] = 1

    return result
