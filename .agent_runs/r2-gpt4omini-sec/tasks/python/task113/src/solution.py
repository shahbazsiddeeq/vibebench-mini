# src/solution.py

def from_roman(s: str) -> int:
    if not s:
        raise ValueError("Input cannot be empty.")
    
    # Define valid Roman numeral characters and their values
    roman_numerals = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    
    # Validate input: only allow valid Roman numeral characters
    if any(char not in roman_numerals for char in s):
        raise ValueError("Invalid characters in input.")
    
    total = 0
    prev_value = 0
    
    # Process the Roman numeral string from right to left
    for char in reversed(s):
        value = roman_numerals[char]
        
        # If the current value is less than the previous value, subtract it
        if value < prev_value:
            total -= value
        else:
            total += value
        
        prev_value = value
    
    return total
