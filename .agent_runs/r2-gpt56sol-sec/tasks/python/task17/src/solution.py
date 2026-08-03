"""Natural sorting utilities."""

from collections.abc import Iterable
import unicodedata


def _numeric_key(digits: list[int]) -> tuple[int, bytes]:
    """Return an integer-free key representing a non-negative decimal value."""
    first_nonzero = 0
    while first_nonzero < len(digits) and digits[first_nonzero] == 0:
        first_nonzero += 1

    significant = bytes(digits[first_nonzero:])
    return len(significant), significant


def _natural_key(value: str) -> tuple[tuple[object, ...], ...]:
    chunks: list[tuple[object, ...]] = []
    position = 0

    while position < len(value):
        is_numeric = value[position].isdigit()
        end = position + 1

        while end < len(value) and value[end].isdigit() == is_numeric:
            end += 1

        run = value[position:end]
        if is_numeric:
            digit_values = [unicodedata.digit(character) for character in run]
            significant_length, significant_digits = _numeric_key(digit_values)
            chunks.append((0, significant_length, significant_digits))
        else:
            chunks.append((1, run))

        position = end

    return tuple(chunks)


def natural_sort(items: Iterable[str]) -> list[str]:
    """Return the supplied strings sorted in stable natural order."""
    if isinstance(items, (str, bytes)) or not isinstance(items, Iterable):
        raise TypeError("items must be an iterable of strings")

    values = list(items)
    if any(not isinstance(item, str) for item in values):
        raise TypeError("all items must be strings")

    return sorted(values, key=_natural_key)
