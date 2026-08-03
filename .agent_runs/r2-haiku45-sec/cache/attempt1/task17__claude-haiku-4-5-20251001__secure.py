import re
from typing import List


def natural_sort(items: List[str]) -> List[str]:
    """
    Sort a list of strings in natural order.
    
    Natural order compares embedded runs of digits by numeric value,
    while runs of non-digit characters are compared lexicographically.
    At the same position, numeric runs sort before text runs.
    The sort is stable and case-sensitive.
    
    Args:
        items: A list of strings to sort
        
    Returns:
        A new list containing the same strings sorted in natural order
    """
    if not items:
        return []
    
    # Validate input
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    
    for item in items:
        if not isinstance(item, str):
            raise TypeError("all items must be strings")
    
    def natural_key(s: str) -> tuple:
        """
        Convert a string into a tuple of comparable elements.
        
        Splits the string into alternating runs of digits and non-digits.
        Digit runs are converted to integers for numeric comparison.
        Non-digit runs remain as strings for lexicographic comparison.
        At the same position, numeric runs (type 0) sort before text runs (type 1).
        """
        parts = []
        # Split on digit boundaries while keeping the delimiters
        for match in re.finditer(r'(\d+|[^\d]+)', s):
            token = match.group(0)
            if token.isdigit():
                # Numeric run: use type 0 (sorts before text) and numeric value
                parts.append((0, int(token)))
            else:
                # Text run: use type 1 (sorts after numeric) and the string itself
                parts.append((1, token))
        return tuple(parts)
    
    # Create a new sorted list using the natural key
    return sorted(items, key=natural_key)
