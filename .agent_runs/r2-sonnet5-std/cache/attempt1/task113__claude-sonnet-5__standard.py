def from_roman(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("Input must be a non-empty string")

    values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    s = s.upper()
    total = 0
    prev_value = 0

    for char in reversed(s):
        if char not in values:
            raise ValueError(f"Invalid Roman numeral character: {char}")
        value = values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total
