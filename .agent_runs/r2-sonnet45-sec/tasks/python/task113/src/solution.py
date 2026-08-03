def from_roman(s: str) -> int:
    """
    Convert a Roman numeral string to an integer.
    
    Args:
        s: A string containing a valid Roman numeral
        
    Returns:
        The integer value of the Roman numeral
        
    Raises:
        ValueError: If the input is empty or contains invalid characters
    """
    if not s:
        raise ValueError("Input string cannot be empty")
    
    # Define valid Roman numeral symbols and their values
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    # Validate input - check all characters are valid Roman numerals
    for char in s:
        if char not in roman_values:
            raise ValueError(f"Invalid character in Roman numeral: {char}")
    
    total = 0
    prev_value = 0
    
    # Process the string from right to left
    for char in reversed(s):
        current_value = roman_values[char]
        
        # If current value is less than previous, subtract it (subtractive notation)
        # Otherwise, add it
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        
        prev_value = current_value
    
    return total
