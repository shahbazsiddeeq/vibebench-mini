ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen"]

TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
        "eighty", "ninety"]

SCALES = ["", "thousand", "million", "billion"]


def _three_digit_to_words(n: int) -> str:
    parts = []
    hundreds = n // 100
    rest = n % 100
    if hundreds:
        parts.append(ONES[hundreds])
        parts.append("hundred")
    if rest:
        if rest < 20:
            parts.append(ONES[rest])
        else:
            tens_digit = rest // 10
            ones_digit = rest % 10
            if ones_digit:
                parts.append(f"{TENS[tens_digit]}-{ONES[ones_digit]}")
            else:
                parts.append(TENS[tens_digit])
    return " ".join(parts)


def number_to_words(n: int) -> str:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < -999999999999 or n > 999999999999:
        raise ValueError("n out of supported range")
    if n == 0:
        return "zero"

    negative = n < 0
    n = abs(n)

    groups = []
    while n > 0:
        groups.append(n % 1000)
        n //= 1000

    parts = []
    for i in range(len(groups) - 1, -1, -1):
        group = groups[i]
        if group == 0:
            continue
        group_words = _three_digit_to_words(group)
        if SCALES[i]:
            parts.append(f"{group_words} {SCALES[i]}")
        else:
            parts.append(group_words)

    result = " ".join(parts)
    if negative:
        result = "negative " + result
    return result
