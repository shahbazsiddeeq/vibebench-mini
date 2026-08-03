def int_to_base(n: int, base: int) -> str:
    """
    Converts a non-negative integer to a string in the given base (2-36).
    Uses digits 0-9 then a-z.

    Args:
        n: The non-negative integer to convert.
        base: The base to convert to (must be between 2 and 36, inclusive).

    Returns:
        A string representation of the integer in the specified base.

    Raises:
        ValueError: If n is negative or base is out of the range [2, 36].
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    if not (2 <= base <= 36):
        raise ValueError("base must be between 2 and 36, inclusive.")

    if n == 0:
        return "0"

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []

    while n > 0:
        remainder = n % base
        result.append(digits[remainder])
        n //= base

    return "".join(result[::-1])
