"""Utilities for validating balanced brackets."""


def is_balanced(s: str) -> bool:
    """Return whether all (), [], and {} brackets in *s* are properly nested."""
    opening = {"(": ")", "[": "]", "{": "}"}
    closing = set(opening.values())
    stack: list[str] = []

    for char in s:
        if char in opening:
            stack.append(opening[char])
        elif char in closing:
            if not stack or stack.pop() != char:
                return False

    return not stack
