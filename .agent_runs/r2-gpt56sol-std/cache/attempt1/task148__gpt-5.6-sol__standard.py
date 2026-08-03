"""Utilities for parsing compact duration strings."""

_UNIT_SECONDS = {
    "w": 604_800,
    "d": 86_400,
    "h": 3_600,
    "m": 60,
    "s": 1,
}


def parse_duration(text: str) -> int:
    """Parse a compact duration string and return its total seconds.

    Raises:
        ValueError: If *text* does not fully conform to the duration grammar.
    """
    if not isinstance(text, str) or not text:
        raise ValueError("invalid duration")

    total = 0
    number = 0
    has_digits = False

    for char in text:
        if "0" <= char <= "9":
            number = number * 10 + (ord(char) - ord("0"))
            has_digits = True
        elif char in _UNIT_SECONDS and has_digits:
            total += number * _UNIT_SECONDS[char]
            number = 0
            has_digits = False
        else:
            raise ValueError("invalid duration")

    if has_digits:
        raise ValueError("invalid duration")

    return total
