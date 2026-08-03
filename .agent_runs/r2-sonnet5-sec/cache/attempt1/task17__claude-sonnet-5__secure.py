import re
from typing import List


def _tokenize(s: str):
    """Split a string into alternating runs of digits and non-digits.

    Each digit run is represented as (0, int_value) so that numeric runs
    compare by their integer value and always sort before text runs at
    the same position (since 0 < 1 as the first tuple element).
    Each non-digit run is represented as (1, run_string) so it compares
    character-by-character by Unicode code point.
    """
    tokens = re.findall(r"\d+|\D+", s)
    key = []
    for tok in tokens:
        if tok.isdigit():
            key.append((0, int(tok)))
        else:
            key.append((1, tok))
    return tuple(key)


def natural_sort(items: List[str]) -> List[str]:
    """Return a new list with items sorted in natural order.

    Numeric runs within each string are compared by their integer value,
    while non-digit runs are compared by Unicode code point. Sorting is
    stable, and case-sensitive (uppercase before lowercase). Inputs with
    mismatched digit/text runs at the same position are handled safely.
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list of strings")

    for item in items:
        if not isinstance(item, str):
            raise TypeError("all elements of items must be strings")

    return sorted(items, key=_tokenize)
