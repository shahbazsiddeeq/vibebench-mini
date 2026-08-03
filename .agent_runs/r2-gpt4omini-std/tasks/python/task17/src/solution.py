# src/solution.py

import re
from typing import List

def natural_sort(items: List[str]) -> List[str]:
    def key_func(item: str):
        # Split the item into parts of digits and non-digits
        return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', item)]
    
    return sorted(items, key=key_func)
