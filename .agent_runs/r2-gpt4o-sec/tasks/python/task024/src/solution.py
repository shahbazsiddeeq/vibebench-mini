# src/solution.py

from typing import List
import bisect

def count_occurrences(arr: List[int], target: int) -> int:
    if not isinstance(arr, list) or not all(isinstance(x, int) for x in arr):
        raise ValueError("Input must be a list of integers.")
    if not isinstance(target, int):
        raise ValueError("Target must be an integer.")
    
    left_index = bisect.bisect_left(arr, target)
    right_index = bisect.bisect_right(arr, target)
    
    return right_index - left_index
