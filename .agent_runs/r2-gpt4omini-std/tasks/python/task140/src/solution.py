# src/solution.py

def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    if not nums:
        raise ValueError("Input list cannot be empty.")
    
    max_sum = current_sum = nums[0]
    start = end = temp_start = 0
    
    for i in range(1, len(nums)):
        if current_sum < 0:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum += nums[i]
        
        if (current_sum > max_sum or 
            (current_sum == max_sum and (temp_start < start or 
            (temp_start == start and i < end)))):
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, start, end
