_ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
    "eighty", "ninety",
]
_SCALES = [(10 ** 9, "billion"), (10 ** 6, "million"), (10 ** 3, "thousand"), (1, "")]
_LIMIT = 999999999999


def _three(num: int) -> str:
    """Words for 1..999 (no leading/trailing spaces)."""
    words = []
    hundreds, rest = divmod(num, 100)
    if hundreds:
        words.append(_ONES[hundreds])
        words.append("hundred")
    if rest:
        if rest < 20:
            words.append(_ONES[rest])
        else:
            tens, ones = divmod(rest, 10)
            if ones:
                words.append(f"{_TENS[tens]}-{_ONES[ones]}")
            else:
                words.append(_TENS[tens])
    return " ".join(words)


def number_to_words(n: int) -> str:
    """Spell an integer in lowercase American English words."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < -_LIMIT or n > _LIMIT:
        raise ValueError("n out of supported range")
    if n == 0:
        return "zero"

    negative = n < 0
    value = -n if negative else n

    parts = []
    for divisor, name in _SCALES:
        group, value = divmod(value, divisor)
        if group:
            chunk = _three(group)
            if name:
                chunk = f"{chunk} {name}"
            parts.append(chunk)
    result = " ".join(parts)
    if negative:
        result = f"negative {result}"
    return result
