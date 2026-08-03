"""Natural sorting utilities."""

from collections.abc import Iterable
from unicodedata import digit


def _natural_key(value: str) -> tuple:
    tokens = []
    index = 0

    while index < len(value):
        is_numeric = value[index].isdigit()
        end = index + 1

        while end < len(value) and value[end].isdigit() == is_numeric:
            end += 1

        run = value[index:end]

        if is_numeric:
            digits = tuple(digit(character) for character in run)
            first_nonzero = 0
            while first_nonzero < len(digits) and digits[first_nonzero] == 0:
                first_nonzero += 1
            significant = digits[first_nonzero:]
            tokens.append((0, len(significant), significant))
        else:
            tokens.append((1, run))

        index = end

    return tuple(tokens)


def natural_sort(items: Iterable[str]) -> list[str]:
    """Return the strings in stable natural-sort order."""
    return sorted(items, key=_natural_key)
