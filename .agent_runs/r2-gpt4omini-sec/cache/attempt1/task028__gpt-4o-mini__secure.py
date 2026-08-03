# src/solution.py

from typing import List
import secrets

def quicksort(lst: List[int]) -> List[int]:
    if not isinstance(lst, list):
        raise ValueError("Input must be a list.")
    
    for item in lst:
        if not isinstance(item, int):
            raise ValueError("All items in the list must be integers.")
    
    if len(lst) <= 1:
        return lst
    
    pivot = secrets.choice(lst)
    less_than_pivot = [x for x in lst if x < pivot]
    equal_to_pivot = [x for x in lst if x == pivot]
    greater_than_pivot = [x for x in lst if x > pivot]
    
    return quicksort(less_than_pivot) + equal_to_pivot + quicksort(greater_than_pivot)
