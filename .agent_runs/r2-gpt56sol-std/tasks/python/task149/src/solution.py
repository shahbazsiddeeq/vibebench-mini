"""Convert integers in the supported range to lowercase American English words."""

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
_MAX_VALUE = 999_999_999_999


def _three_digit_group_to_words(value: int) -> str:
    """Return words for an integer from 1 through 999."""
    parts = []

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
            word += "-" + _ONES[ones]
        parts.append(word)

    return " ".join(parts)


def number_to_words(n: int) -> str:
    """Spell a supported whole number in lowercase American English."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < -_MAX_VALUE or n > _MAX_VALUE:
        raise ValueError("n is outside the supported range")
    if n == 0:
        return "zero"
    if n < 0:
        return "negative " + number_to_words(-n)

    groups = []
    scale_index = 0

    while n:
        n, group = divmod(n, 1000)
        if group:
            words = _three_digit_group_to_words(group)
            scale = _SCALES[scale_index]
            if scale:
                words += " " + scale
            groups.append(words)
        scale_index += 1

    return " ".join(reversed(groups))
