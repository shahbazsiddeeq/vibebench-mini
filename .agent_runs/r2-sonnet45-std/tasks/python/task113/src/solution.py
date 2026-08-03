def from_roman(s: str) -> int:
    """Convert a Roman numeral string to an integer.
    
    Args:
        s: Roman numeral string
        
    Returns:
        Integer value of the Roman numeral
        
    Raises:
        ValueError: If input is empty or contains invalid characters
    """
    if not s:
        raise ValueError("Input cannot be empty")
    
    # Map of Roman numeral characters to their values
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    # Validate all characters are valid Roman numerals
    for char in s:
        if char not in roman_values:
            raise ValueError(f"Invalid Roman numeral character: {char}")
    
    total = 0
    prev_value = 0
    
    # Process the string from right to left
    for char in reversed(s):
        value = roman_values[char]
        
        # If current value is less than previous, subtract it (subtractive notation)
        # Otherwise, add it
        if value < prev_value:
            total -= value
        else:
            total += value
        
        prev_value = value
    
    return total
