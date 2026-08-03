# src/solution.py

def from_roman(s: str) -> int:
    if not s:
        raise ValueError("Input cannot be empty")
    
    roman_numerals = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    for char in reversed(s):
        if char not in roman_numerals:
            raise ValueError(f"Invalid character '{char}' in input")
        
        value = roman_numerals[char]
        
        if value < prev_value:
            total -= value
        else:
            total += value
        
        prev_value = value
    
    return total
