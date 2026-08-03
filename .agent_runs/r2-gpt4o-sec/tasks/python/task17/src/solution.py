import re
from typing import List

def natural_sort(items: List[str]) -> List[str]:
    def natural_key(s: str):
        # Split the string into parts: sequences of digits and non-digits
        parts = re.split(r'(\d+)', s)
        # Convert digit parts to integers for numeric comparison
        return [(int(part) if part.isdigit() else part) for part in parts]

    # Sort using the natural key
    return sorted(items, key=natural_key)

# Example usage:
# print(natural_sort(["file10", "file2", "file1"]))  # Output: ["file1", "file2", "file10"]
# print(natural_sort(["A2", "a11", "a1b", "a1a"]))  # Output: ["A2", "a1a", "a1b", "a11"]
