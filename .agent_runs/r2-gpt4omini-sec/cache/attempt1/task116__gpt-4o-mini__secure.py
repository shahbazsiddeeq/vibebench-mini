# src/solution.py

from typing import List, Any
from itertools import chain, combinations

def power_set(elements: List[Any]) -> List[frozenset]:
    # Validate input
    if not isinstance(elements, list):
        raise ValueError("Input must be a list.")
    
    # Remove duplicates by converting to a set, then back to a sorted list
    unique_elements = sorted(set(elements))
    
    # Generate all combinations of the unique elements
    all_subsets = list(chain.from_iterable(combinations(unique_elements, r) for r in range(len(unique_elements) + 1)))
    
    # Convert combinations to frozensets
    power_set_result = [frozenset(subset) for subset in all_subsets]
    
    # Sort the result first by size, then lexicographically
    power_set_result.sort(key=lambda x: (len(x), tuple(sorted(x))))
    
    return power_set_result
