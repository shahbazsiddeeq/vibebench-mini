# src/solution.py

def two_sum(nums, target):
    index_map = {}
    
    for j, num in enumerate(nums):
        complement = target - num
        
        if complement in index_map:
            i = index_map[complement]
            return (i, j)
        
        # Store the index of the current number
        index_map[num] = j
    
    raise ValueError("No two sum solution")
