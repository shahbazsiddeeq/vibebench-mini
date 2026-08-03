def two_sum(nums, target):
    num_to_index = {}
    
    for j, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            i = num_to_index[complement]
            return (i, j)
        num_to_index[num] = j
    
    raise ValueError("No two sum solution")
