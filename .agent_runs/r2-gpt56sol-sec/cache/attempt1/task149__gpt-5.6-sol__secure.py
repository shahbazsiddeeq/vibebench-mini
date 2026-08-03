"""Convert supported integers to lowercase American English words."""

_ONES = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
)

_TENS = (
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
)

_SCALES = ("", "thousand", "million", "billion")
_LIMIT = 999_999_999_999


def _group_to_words(value: int) -> str:
    """Convert an integer from 1 through 999 to words."""
    parts: list[str] = []

    hundreds, remainder = divmod(value, 100)
    if hundreds:
        parts.extend((_ONES[hundreds], "hundred"))

    if remainder < 20:
        if remainder:
            parts.append(_ONES[remainder])
    else:
        tens, ones = divmod(remainder, 10)
        word = _TENS[tens]
        if ones:
            word = f"{word}-{_ONES[ones]}"
        parts.append(word)

    return " ".join(parts)


def number_to_words(n: int) -> str:
    """Spell a supported whole number in lowercase American English."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if not -_LIMIT <= n <= _LIMIT:
        raise ValueError("n is outside the supported range")

    if n == 0:
        return "zero"

    negative = n < 0
    value = abs(n)
    groups: list[str] = []
    scale_index = 0

    while value:
        value, group = divmod(value, 1000)
        if group:
            words = _group_to_words(group)
            scale = _SCALES[scale_index]
            groups.append(f"{words} {scale}" if scale else words)
        scale_index += 1

    result = " ".join(reversed(groups))
    return f"negative {result}" if negative else result


__all__ = ["number_to_words"]
