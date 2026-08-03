"""
Balanced Parentheses checker.

This module provides a single public function, `is_balanced`, which
determines whether the bracket characters in a given string are
properly nested and matched. Non-bracket characters are ignored.

Security considerations:
- Input is validated to be a string; no eval/exec or dynamic code execution.
- No I/O operations are performed.
- Function is pure and side-effect free.
- Errors are raised with generic, non-sensitive messages (no internal
  state or stack traces are exposed to callers).
"""

from typing import Dict


_OPENERS = "([{"
_CLOSERS = ")]}"
_PAIRS: Dict[str, str] = {
    ")": "(",
    "]": "[",
    "}": "{",
}


def is_balanced(s: str) -> bool:
    """
    Determine whether all bracket characters in `s` are properly
    nested and matched.

    Supported bracket types: (), [], {}
    Any other characters in the string are ignored.

    Args:
        s: The input string to check.

    Returns:
        True if brackets are balanced and properly nested, False otherwise.

    Raises:
        TypeError: If `s` is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    stack = []

    for char in s:
        if char in _OPENERS:
            stack.append(char)
        elif char in _CLOSERS:
            if not stack:
                return False
            expected_opener = _PAIRS[char]
            top = stack.pop()
            if top != expected_opener:
                return False
        # Non-bracket characters are ignored entirely.

    return len(stack) == 0
