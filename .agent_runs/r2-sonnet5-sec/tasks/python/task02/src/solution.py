"""
src/solution.py

A secure, self-contained module implementing reverse_words.

Design notes (security-focused):
- Only uses the Python standard library.
- No eval/exec, no dynamic code execution.
- No file, network, or subprocess I/O.
- Strict input validation: only str instances are processed; any other
  type raises a clear TypeError without leaking internal state details.
- Uses str.split() (no argument) which safely splits on any whitespace
  run and discards leading/trailing whitespace, avoiding manual parsing
  bugs or regex-based ReDoS risks.
"""

from typing import List


def reverse_words(s: str) -> str:
    """
    Reverse the order of whitespace-separated words in the input string.

    Words are maximal runs of non-whitespace characters. Any run of
    whitespace (spaces, tabs, newlines, etc.) acts as a separator and is
    collapsed to a single space in the output. Leading and trailing
    whitespace is ignored. If the input is empty or contains only
    whitespace, an empty string is returned.

    Args:
        s: The input string to process.

    Returns:
        A string with words in reverse order, joined by a single space,
        or "" if there are no words.

    Raises:
        TypeError: If `s` is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("reverse_words expects a string input")

    # str.split() with no arguments splits on any whitespace run and
    # ignores leading/trailing whitespace, safely handling all whitespace
    # types without risk of catastrophic backtracking (no regex used).
    words: List[str] = s.split()

    return " ".join(reversed(words))
