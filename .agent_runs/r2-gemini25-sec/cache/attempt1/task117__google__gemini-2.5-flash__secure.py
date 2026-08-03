import math

def int_to_base(n: int, base: int) -> str:
    """
    Converts a non-negative integer to a string in the given base (2-36).
    Uses digits 0-9 then a-z.

    Args:
        n: The non-negative integer to convert.
        base: The base for the conversion (must be between 2 and 36, inclusive).

    Returns:
        A string representation of the integer in the specified base.

    Raises:
        ValueError: If n is negative or base is out of the range [2, 36].
    """
    if not isinstance(n, int) or not isinstance(base, int):
        raise ValueError("Inputs n and base must be integers.")

    if n < 0:
        raise ValueError("Input n must be a non-negative integer.")
    if not (2 <= base <= 36):
        raise ValueError("Input base must be between 2 and 36 (inclusive).")

    if n == 0:
        return "0"

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []

    while n > 0:
        remainder = n % base
        result.append(digits[remainder])
        n //= base

    return "".join(reversed(result))
