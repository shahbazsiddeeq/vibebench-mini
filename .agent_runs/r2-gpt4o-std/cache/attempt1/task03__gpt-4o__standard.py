# src/solution.py

import re

def is_palindrome(s: str) -> bool:
    # Use regular expression to filter only alphanumeric ASCII characters
    filtered = re.sub(r'[^A-Za-z0-9]', '', s).lower()
    # Check if the filtered string is equal to its reverse
    return filtered == filtered[::-1]
