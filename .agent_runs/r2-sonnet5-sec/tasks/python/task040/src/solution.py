"""
Roman Numeral Converter

Provides a single function, to_roman, that converts an integer in the
range 1-3999 (inclusive) into its Roman numeral string representation.

Security considerations:
- Strict input validation (type and range checks) before processing.
- No use of eval/exec or any dynamic code execution.
- No external I/O; the function is pure and side-effect free.
- Errors are raised with generic, non-revealing messages to avoid
  leaking internal implementation details.
"""

from typing import List, Tuple

# Ordered mapping of value -> Roman numeral symbol, from largest to smallest.
_ROMAN_TABLE: Tuple[Tuple[int, str], ...] = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_MIN_VALUE = 1
_MAX_VALUE = 3999


def to_roman(n: int) -> str:
    """
    Convert an integer between 1 and 3999 (inclusive) to a Roman numeral.

    Args:
        n: Integer to convert.

    Returns:
        The Roman numeral representation of n as a string.

    Raises:
        ValueError: If n is not an integer, or is outside the range
            1-3999 (inclusive).
    """
    # Reject booleans explicitly (bool is a subclass of int) and any
    # non-integer types to keep behavior predictable and safe.
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("Input must be an integer between 1 and 3999.")

    if n < _MIN_VALUE or n > _MAX_VALUE:
        raise ValueError("Input must be an integer between 1 and 3999.")

    result: List[str] = []
    remaining = n

    for value, symbol in _ROMAN_TABLE:
        if remaining <= 0:
            break
        count, remaining = divmod(remaining, value)
        if count:
            result.append(symbol * count)

    return "".join(result)
