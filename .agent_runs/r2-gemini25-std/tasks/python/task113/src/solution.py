def from_roman(s: str) -> int:
    """
    Converts a Roman numeral string to an integer.

    Raises ValueError for empty input or invalid characters.

    Example:
    from_roman("XIV") -> 14
    from_roman("IV") -> 4
    """
    if not s:
        raise ValueError("Input string cannot be empty.")

    roman_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    result = 0
    prev_value = 0

    for char in reversed(s):
        if char not in roman_map:
            raise ValueError(f"Invalid Roman numeral character: {char}")
        
        current_value = roman_map[char]

        if current_value < prev_value:
            result -= current_value
        else:
            result += current_value
        
        prev_value = current_value
    
    return result
