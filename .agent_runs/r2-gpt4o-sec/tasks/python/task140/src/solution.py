import secrets
from typing import List, Tuple

def max_subarray(nums: List[int]) -> Tuple[int, int, int]:
    if not nums:
        raise ValueError("The input list cannot be empty.")
    
    max_sum = float('-inf')
    current_sum = 0
    start = 0
    best_start = 0
    best_end = 0
    
    for i, num in enumerate(nums):
        if current_sum <= 0:
            current_sum = num
            start = i
        else:
            current_sum += num
        
        if (current_sum > max_sum or 
            (current_sum == max_sum and (i - start < best_end - best_start))):
            max_sum = current_sum
            best_start = start
            best_end = i
    
    return max_sum, best_start, best_end
