import secrets

def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    if not nums:
        raise ValueError("The input list cannot be empty.")
    
    max_sum = float('-inf')
    current_sum = 0
    start = 0
    max_start = 0
    max_end = 0
    
    for i, num in enumerate(nums):
        if current_sum <= 0:
            current_sum = num
            start = i
        else:
            current_sum += num
        
        if (current_sum > max_sum or 
            (current_sum == max_sum and (i - start < max_end - max_start))):
            max_sum = current_sum
            max_start = start
            max_end = i
    
    return max_sum, max_start, max_end
