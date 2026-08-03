"""Utilities for converting non-negative integers to other bases."""

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def int_to_base(n: int, base: int) -> str:
    """Convert a non-negative integer to a base-2 through base-36 string."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if not isinstance(base, int) or isinstance(base, bool):
        raise TypeError("base must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if not 2 <= base <= 36:
        raise ValueError("base must be between 2 and 36")
    if n == 0:
        return "0"

    result = []
    while n:
        n, remainder = divmod(n, base)
        result.append(DIGITS[remainder])

    return "".join(reversed(result))
