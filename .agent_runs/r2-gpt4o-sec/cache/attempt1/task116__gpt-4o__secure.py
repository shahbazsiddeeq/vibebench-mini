from itertools import chain, combinations
from typing import List, Any
import secrets

def power_set(elements: List[Any]) -> List[frozenset]:
    # Remove duplicates by converting to a set
    unique_elements = set(elements)
    
    # Generate all combinations of the unique elements
    all_combinations = chain.from_iterable(combinations(unique_elements, r) for r in range(len(unique_elements) + 1))
    
    # Convert each combination to a frozenset
    power_set_list = [frozenset(comb) for comb in all_combinations]
    
    # Sort by size and then lexicographically by string representation
    power_set_list.sort(key=lambda s: (len(s), sorted(str(e) for e in s)))
    
    return power_set_list
