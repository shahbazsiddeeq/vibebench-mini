"""Roman numeral conversion utilities."""


def to_roman(n: int) -> str:
    """Convert an integer from 1 through 3999 to a Roman numeral.

    Raises:
        ValueError: If *n* is not an integer in the supported range.
    """
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 3999:
        raise ValueError("n must be an integer between 1 and 3999")

    values = (
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
    for value, numeral in values:
        count, n = divmod(n, value)
        result.append(numeral * count)

    return "".join(result)
