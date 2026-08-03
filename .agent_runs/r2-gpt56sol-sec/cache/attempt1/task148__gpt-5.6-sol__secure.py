"""Utilities for parsing compact duration strings."""

_UNIT_SECONDS = {
    "w": 604_800,
    "d": 86_400,
    "h": 3_600,
    "m": 60,
    "s": 1,
}


def parse_duration(text: str) -> int:
    """Convert a compact duration string to its total number of seconds.

    Raises:
        ValueError: If *text* does not fully conform to the duration grammar.
    """
    if not isinstance(text, str) or not text:
        raise ValueError("invalid duration")

    total = 0
    number = 0
    has_digits = False

    for character in text:
        if "0" <= character <= "9":
            number = number * 10 + (ord(character) - ord("0"))
            has_digits = True
            continue

        multiplier = _UNIT_SECONDS.get(character)
        if multiplier is None or not has_digits:
            raise ValueError("invalid duration")

        total += number * multiplier
        number = 0
        has_digits = False

    if has_digits:
        raise ValueError("invalid duration")

    return total
