def two_sum(nums, target):
    if not isinstance(nums, list) or not all(isinstance(x, int) for x in nums):
        raise ValueError("Input must be a list of integers.")
    if not isinstance(target, int):
        raise ValueError("Target must be an integer.")

    index_map = {}
    for j, num in enumerate(nums):
        complement = target - num
        if complement in index_map:
            i = index_map[complement]
            return (i, j)
        index_map[num] = j

    raise ValueError("No two sum solution exists.")
