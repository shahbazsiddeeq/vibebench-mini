def from_roman(s: str) -> int:
    """
    Convert a Roman numeral string to an integer.
    
    Args:
        s: A Roman numeral string (e.g., "XIV", "IV")
    
    Returns:
        The integer value of the Roman numeral
    
    Raises:
        ValueError: If the input is empty or contains invalid characters
    """
    # Validate input
    if not s:
        raise ValueError("Roman numeral string cannot be empty")
    
    # Define valid Roman numeral characters
    valid_chars = set("IVXLCDM")
    
    # Check for invalid characters
    if not all(c in valid_chars for c in s):
        raise ValueError("Invalid characters in Roman numeral string")
    
    # Define the mapping of Roman numerals to their values
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }
    
    total = 0
    prev_value = 0
    
    # Process the string from right to left
    for char in reversed(s):
        current_value = roman_values[char]
        
        # If current value is less than previous value, subtract it (subtractive notation)
        # Otherwise, add it
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        
        prev_value = current_value
    
    return total
