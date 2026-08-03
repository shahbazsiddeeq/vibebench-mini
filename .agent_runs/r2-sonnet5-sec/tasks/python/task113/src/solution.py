"""
Roman Numeral Decoder

Provides `from_roman(s)` which converts a valid Roman numeral string to its
integer value. Raises ValueError for empty input, invalid characters, or
malformed Roman numerals.

This module is intentionally defensive: it validates all external input
strictly, does not use eval/exec, and never exposes internal implementation
details in error messages beyond what's needed to indicate invalid input.
"""

import re

# Precompiled regex for valid Roman numerals from 1 to 3999.
# This strictly validates the structure (correct subtractive notation,
# no repeated numerals beyond allowed counts, correct symbol ordering).
_ROMAN_PATTERN = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)

# Mapping of individual Roman numeral symbols to their integer values.
_SYMBOL_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def from_roman(s: str) -> int:
    """
    Convert a Roman numeral string to an integer.

    Args:
        s: A string representing a Roman numeral (e.g., "XIV").

    Returns:
        The integer value of the Roman numeral.

    Raises:
        ValueError: If the input is empty, not a string, contains invalid
            characters, or is not a well-formed Roman numeral.
    """
    if not isinstance(s, str):
        raise ValueError("Invalid Roman numeral: input must be a string")

    if len(s) == 0:
        raise ValueError("Invalid Roman numeral: input is empty")

    # Normalize case defensively, but only accept uppercase canonical form
    # to avoid ambiguity; reject lowercase/mixed input explicitly by
    # checking against allowed characters first.
    for ch in s:
        if ch not in _SYMBOL_VALUES:
            raise ValueError("Invalid Roman numeral: contains invalid characters")

    if not _ROMAN_PATTERN.match(s):
        raise ValueError("Invalid Roman numeral: malformed numeral")

    total = 0
    i = 0
    length = len(s)
    while i < length:
        # Check for two-character subtractive pairs first.
        if i + 1 < length:
            two_char = s[i:i + 2]
            pair_value = _SUBTRACTIVE_PAIRS.get(two_char)
            if pair_value is not None:
                total += pair_value
                i += 2
                continue
        total += _SYMBOL_VALUES[s[i]]
        i += 1

    return total


# Mapping of valid subtractive pairs to their combined integer values.
_SUBTRACTIVE_PAIRS = {
    "CM": 900,
    "CD": 400,
    "XC": 90,
    "XL": 40,
    "IX": 9,
    "IV": 4,
}
