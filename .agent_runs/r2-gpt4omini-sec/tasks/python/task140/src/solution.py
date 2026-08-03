# src/solution.py

def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    if not isinstance(nums, list) or not all(isinstance(x, int) for x in nums):
        raise ValueError("Input must be a list of integers.")
    
    if len(nums) == 0:
        raise ValueError("Input list cannot be empty.")
    
    max_sum = float('-inf')
    current_sum = 0
    start = 0
    best_start = 0
    best_end = 0
    
    for i, num in enumerate(nums):
        current_sum += num
        
        if current_sum > max_sum:
            max_sum = current_sum
            best_start = start
            best_end = i
        elif current_sum == max_sum:
            if (i - start) < (best_end - best_start):
                best_start = start
                best_end = i
        
        if current_sum < 0:
            current_sum = 0
            start = i + 1
    
    return max_sum, best_start, best_end
