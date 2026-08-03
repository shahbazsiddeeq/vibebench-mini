def number_to_words(n: int) -> str:
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("Input must be an integer.")

    if not (-999999999999 <= n <= 999999999999):
        raise ValueError("Input number out of supported range.")

    if n == 0:
        return "zero"

    negative = False
    if n < 0:
        negative = True
        n = abs(n)

    words = []
    if negative:
        words.append("negative")

    def _convert_less_than_thousand(num: int) -> str:
        if num == 0:
            return ""

        _ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        _teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
        _tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        part_words = []
        if num >= 100:
            part_words.append(_ones[num // 100])
            part_words.append("hundred")
            num %= 100

        if num >= 20:
            if num % 10 == 0:
                part_words.append(_tens[num // 10])
            else:
                part_words.append(f"{_tens[num // 10]}-{_ones[num % 10]}")
        elif num >= 10:
            part_words.append(_teens[num - 10])
        elif num > 0:
            part_words.append(_ones[num])

        return " ".join(part_words)

    billions = n // 1_000_000_000
    n %= 1_000_000_000
    millions = n // 1_000_000
    n %= 1_000_000
    thousands = n // 1_000
    n %= 1_000
    remainder = n

    if billions > 0:
        words.append(_convert_less_than_thousand(billions))
        words.append("billion")
    if millions > 0:
        words.append(_convert_less_than_thousand(millions))
        words.append("million")
    if thousands > 0:
        words.append(_convert_less_than_thousand(thousands))
        words.append("thousand")
    if remainder > 0:
        words.append(_convert_less_than_thousand(remainder))

    # Filter out empty strings that might result from _convert_less_than_thousand for zero groups
    # and join with single spaces.
    result = " ".join(filter(None, words))

    # Handle cases like "negative zero" if n was 0 and negative, though 0 is handled separately.
    # This also cleans up potential double spaces if a group was skipped.
    return result.replace("  ", " ").strip()
