def number_to_words(n: int) -> str:
    """
    Spells a whole number in lowercase American English.

    Args:
        n: The integer to convert to words.

    Returns:
        A string representing the number in words.

    Raises:
        TypeError: If n is not an int (bool is rejected too).
        ValueError: If n is outside the supported range -999,999,999,999 to 999,999,999,999.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("Input must be an integer.")

    MIN_VALUE = -999999999999
    MAX_VALUE = 999999999999

    if not (MIN_VALUE <= n <= MAX_VALUE):
        raise ValueError(f"Input must be between {MIN_VALUE} and {MAX_VALUE} inclusive.")

    if n == 0:
        return "zero"

    negative = False
    if n < 0:
        negative = True
        n = abs(n)

    words = []

    # Define word mappings
    _ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    _teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    _tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    _thousands_suffixes = ["", "thousand", "million", "billion"]

    def _convert_less_than_thousand(num: int) -> str:
        part_words = []
        if num >= 100:
            part_words.append(_ones[num // 100])
            part_words.append("hundred")
            num %= 100

        if num >= 20:
            part_words.append(_tens[num // 10])
            if num % 10 > 0:
                part_words.append(_ones[num % 10])
        elif num >= 10:
            part_words.append(_teens[num - 10])
        elif num > 0:
            part_words.append(_ones[num])
        
        # Join hyphenated parts if applicable (e.g., twenty-one)
        if len(part_words) >= 2 and part_words[-2] in _tens[2:] and part_words[-1] in _ones[1:]:
            last_two = f"{part_words[-2]}-{part_words[-1]}"
            return " ".join(part_words[:-2] + [last_two])
        
        return " ".join(part_words)

    parts = []
    group_index = 0
    while n > 0:
        chunk = n % 1000
        if chunk > 0:
            chunk_words = _convert_less_than_thousand(chunk)
            if group_index > 0:
                if chunk_words: # Only add suffix if chunk_words is not empty
                    parts.append(f"{chunk_words} {_thousands_suffixes[group_index]}")
            else:
                parts.append(chunk_words)
        n //= 1000
        group_index += 1

    result = " ".join(reversed(parts))

    if negative:
        return f"negative {result}"
    else:
        return result
