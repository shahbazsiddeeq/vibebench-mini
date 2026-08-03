"""
src/solution.py

A secure, self-contained implementation of a recursive list flattening
utility.

The `flatten` function takes an arbitrarily deeply nested list and
returns a single flat list containing all non-list elements, preserving
their order. Non-list items pass through unchanged.

Security considerations:
- Input validation: only `list` instances are recursed into; all other
  types are treated as opaque leaf values and passed through unchanged.
- No use of eval/exec or any dynamic code execution.
- No I/O operations (no prints, file access, network calls, etc.).
- Recursion depth is bounded by a configurable limit to avoid
  uncontrolled resource consumption (denial-of-service via stack
  overflow) on maliciously deep or adversarial input structures.
- Errors are raised with generic, non-sensitive messages that do not
  leak internal implementation details.
"""

from typing import Any, List

# A conservative limit to guard against pathological inputs (e.g.,
# extremely deep nested lists) that could otherwise exhaust the call
# stack and crash the interpreter.
_MAX_DEPTH = 1000


def flatten(nested: List[Any], _depth: int = 0) -> List[Any]:
    """
    Recursively flattens an arbitrarily nested list into a single flat list.

    Args:
        nested: A list which may contain nested lists at any depth.
        _depth: Internal parameter tracking recursion depth; not intended
            for external use.

    Returns:
        A new flat list containing all non-list elements from `nested`,
        in order.

    Raises:
        TypeError: If `nested` is not a list.
        RecursionError: If the nesting depth exceeds the safety limit.
    """
    if not isinstance(nested, list):
        raise TypeError("flatten() requires a list as input")

    if _depth > _MAX_DEPTH:
        raise RecursionError("Maximum nesting depth exceeded")

    result: List[Any] = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item, _depth + 1))
        else:
            result.append(item)
    return result
