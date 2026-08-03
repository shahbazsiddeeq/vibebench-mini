"""Utilities for checking balanced brackets."""

from typing import Any


def is_balanced(s: str) -> bool:
    """Return whether brackets in *s* are properly matched and nested.

    Non-bracket characters are ignored.

    Raises:
        TypeError: If *s* is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("s must be a string")

    opening = {"(", "[", "{"}
    matching_open = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for character in s:
        if character in opening:
            stack.append(character)
        elif character in matching_open:
            if not stack or stack.pop() != matching_open[character]:
                return False

    return not stack
