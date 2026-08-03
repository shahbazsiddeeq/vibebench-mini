# src/solution.py

def from_roman(s: str) -> int:
    if not s:
        raise ValueError("Input cannot be empty")

    roman_to_int = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    valid_characters = set(roman_to_int.keys())
    if not all(char in valid_characters for char in s):
        raise ValueError("Invalid characters in input")

    total = 0
    prev_value = 0

    for char in reversed(s):
        value = roman_to_int[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total
