# src/solution.py

import re
from typing import List, Union

def natural_sort(items: List[str]) -> List[str]:
    if not isinstance(items, list):
        raise ValueError("Input must be a list.")
    
    for item in items:
        if not isinstance(item, str):
            raise ValueError("All items in the list must be strings.")
    
    def split_key(s: str) -> List[Union[str, int]]:
        # Split the string into parts of digits and non-digits
        return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', s)]
    
    return sorted(items, key=split_key)
