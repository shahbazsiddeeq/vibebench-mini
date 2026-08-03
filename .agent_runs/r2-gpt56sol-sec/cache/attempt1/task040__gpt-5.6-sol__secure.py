"""Roman numeral conversion utilities."""


def to_roman(n: int) -> str:
    """Convert an integer from 1 through 3999 to a Roman numeral.

    Raises:
        TypeError: If ``n`` is not an integer.
        ValueError: If ``n`` is outside the supported range.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if not 1 <= n <= 3999:
        raise ValueError("n must be between 1 and 3999")

    numerals = (
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

    result = []
    remainder = n

    for value, symbol in numerals:
        count, remainder = divmod(remainder, value)
        if count:
            result.append(symbol * count)

    return "".join(result)
