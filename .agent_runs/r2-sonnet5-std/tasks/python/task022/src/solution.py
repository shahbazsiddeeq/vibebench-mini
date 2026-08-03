def two_sum(nums, target):
    n = len(nums)
    for j in range(1, n):
        for i in range(j - 1, -1, -1):
            if nums[i] + nums[j] == target:
                return (i, j)
    raise ValueError("No two sum solution")
