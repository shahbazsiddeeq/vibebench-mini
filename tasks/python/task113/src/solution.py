def from_roman(s: str) -> int:
    if not s:
        raise ValueError("Empty input")
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    for ch in s:
        if ch not in values:
            raise ValueError(f"Invalid character: {ch!r}")
    result = 0
    prev = 0
    for ch in reversed(s):
        val = values[ch]
        if val < prev:
            result -= val
        else:
            result += val
        prev = val
    return result
