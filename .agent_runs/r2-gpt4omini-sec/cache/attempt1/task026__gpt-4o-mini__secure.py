# src/solution.py

from itertools import permutations as itertools_permutations
from typing import List, Tuple

def permutations(lst: List[int]) -> List[Tuple[int, ...]]:
    if not isinstance(lst, list):
        raise ValueError("Input must be a list.")
    
    if len(lst) > 8:
        raise ValueError("List length must not exceed 8.")
    
    for item in lst:
        if not isinstance(item, int):
            raise ValueError("All elements in the list must be integers.")
    
    # Generate permutations using itertools and convert to sorted list of tuples
    perm = sorted(itertools_permutations(lst))
    
    return list(perm)
