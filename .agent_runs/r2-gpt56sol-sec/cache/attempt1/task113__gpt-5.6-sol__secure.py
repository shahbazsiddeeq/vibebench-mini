"""Roman numeral decoding utilities."""

_ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def from_roman(s: str) -> int:
    """Convert a Roman numeral string to an integer.

    Raises:
        ValueError: If *s* is empty, is not a string, or contains an invalid
            Roman numeral character.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("Roman numeral must be a non-empty string")

    try:
        values = [_ROMAN_VALUES[character] for character in s]
    except KeyError:
        raise ValueError("Roman numeral contains an invalid character") from None

    total = 0
    for index, value in enumerate(values):
        if index + 1 < len(values) and value < values[index + 1]:
            total -= value
        else:
            total += value

    return total
