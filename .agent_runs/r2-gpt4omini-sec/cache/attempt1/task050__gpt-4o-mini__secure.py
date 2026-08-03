# src/solution.py

def unique_char_count(s: str) -> dict:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Dictionary to count occurrences of each character
    char_count = {}
    
    # Count each character in the string
    for char in s:
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("Input string must contain only single characters.")
        char_count[char] = char_count.get(char, 0) + 1
    
    # Create a dictionary for characters that appear exactly once
    unique_chars = {char: 1 for char, count in char_count.items() if count == 1}
    
    return unique_chars
