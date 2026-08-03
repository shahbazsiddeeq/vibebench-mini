def to_roman(n: int) -> str:
    """
    Converts an integer (1-3999) to its Roman numeral representation.

    Args:
        n: An integer between 1 and 3999 (inclusive).

    Returns:
        A string representing the Roman numeral.

    Raises:
        ValueError: If n is outside the range 1-3999.
    """
    if not (1 <= n <= 3999):
        raise ValueError("Input must be an integer between 1 and 3999.")

    roman_map = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I")
    ]

    result = []
    for value, numeral in roman_map:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)
