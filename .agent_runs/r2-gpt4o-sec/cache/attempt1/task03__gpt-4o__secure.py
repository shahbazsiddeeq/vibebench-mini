# src/solution.py

import re

def is_palindrome(s: str) -> bool:
    # Use a regular expression to filter out non-alphanumeric ASCII characters
    filtered = re.sub(r'[^A-Za-z0-9]', '', s)
    # Convert to lowercase
    filtered = filtered.lower()
    # Check if the filtered string is a palindrome
    return filtered == filtered[::-1]
