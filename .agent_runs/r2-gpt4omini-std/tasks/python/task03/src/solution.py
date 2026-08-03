# src/solution.py

import re

def is_palindrome(s: str) -> bool:
    # Filter out non-alphanumeric characters and convert to lowercase
    filtered = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    # Check if the filtered string is equal to its reverse
    return filtered == filtered[::-1]
