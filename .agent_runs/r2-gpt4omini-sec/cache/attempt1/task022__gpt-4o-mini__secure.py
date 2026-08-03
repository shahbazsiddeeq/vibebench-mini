# src/solution.py

def two_sum(nums, target):
    if not isinstance(nums, list) or not all(isinstance(x, (int, float)) for x in nums):
        raise ValueError("nums must be a list of numbers.")
    if not isinstance(target, (int, float)):
        raise ValueError("target must be a number.")
    
    num_to_index = {}
    
    for j, num in enumerate(nums):
        complement = target - num
        
        if complement in num_to_index:
            i = num_to_index[complement]
            return (i, j)
        
        # Store the index of the current number
        num_to_index[num] = j
    
    raise ValueError("No two sum solution exists.")
