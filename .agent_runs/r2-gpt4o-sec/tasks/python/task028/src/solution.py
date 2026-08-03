# src/solution.py

from typing import List

def quicksort(lst: List[int]) -> List[int]:
    if not isinstance(lst, list):
        raise ValueError("Input must be a list.")
    if not all(isinstance(x, int) for x in lst):
        raise ValueError("All elements in the list must be integers.")
    
    def _quicksort(arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return _quicksort(left) + middle + _quicksort(right)
    
    return _quicksort(lst)
