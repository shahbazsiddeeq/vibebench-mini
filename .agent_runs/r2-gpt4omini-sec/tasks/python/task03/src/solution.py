# src/solution.py

import re

def is_palindrome(s: str) -> bool:
    # Validate input type
    if not isinstance(s, str):
        raise ValueError("Input must be a string")

    # Normalize the string: keep only alphanumeric characters and convert to lowercase
    filtered_chars = re.sub(r'[^A-Za-z0-9]', '', s).lower()
    
    # Check if the filtered string is a palindrome
    return filtered_chars == filtered_chars[::-1]
