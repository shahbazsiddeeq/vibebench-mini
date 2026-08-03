"""
Integer to English Words converter.

Provides number_to_words(n: int) -> str which spells out a whole number
in lowercase American English using the short scale.
"""

from __future__ import annotations

MIN_VALUE = -999999999999
MAX_VALUE = 999999999999

_ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]

_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
    "eighty", "ninety",
]

_SCALES = [
    (1_000_000_000, "billion"),
    (1_000_000, "million"),
    (1_000, "thousand"),
]


def _two_digits_to_words(n: int) -> str:
    """Convert a number in [0, 99] to words."""
    if n < 20:
        return _ONES[n]
    tens, remainder = divmod(n, 10)
    if remainder == 0:
        return _TENS[tens]
    return f"{_TENS[tens]}-{_ONES[remainder]}"


def _three_digits_to_words(n: int) -> str:
    """Convert a number in [0, 999] to words."""
    hundreds, remainder = divmod(n, 100)
    parts = []
    if hundreds:
        parts.append(f"{_ONES[hundreds]} hundred")
    if remainder:
        parts.append(_two_digits_to_words(remainder))
    return " ".join(parts)


def number_to_words(n: int) -> str:
    """
    Spell a whole number in lowercase American English (short scale).

    Raises:
        TypeError: if n is not an int (bool is explicitly rejected).
        ValueError: if n is outside [-999999999999, 999999999999].
    """
    # bool is a subclass of int, so explicitly reject it.
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int (bool is not accepted)")

    if n < MIN_VALUE or n > MAX_VALUE:
        raise ValueError(
            f"n must be between {MIN_VALUE} and {MAX_VALUE} inclusive"
        )

    if n == 0:
        return "zero"

    negative = n < 0
    magnitude = -n if negative else n

    parts = []
    remaining = magnitude
    for scale_value, scale_name in _SCALES:
        group, remaining = divmod(remaining, scale_value)
        if group:
            parts.append(f"{_three_digits_to_words(group)} {scale_name}")

    if remaining:
        parts.append(_three_digits_to_words(remaining))

    words = " ".join(parts)

    if negative:
        words = f"negative {words}"

    return words
