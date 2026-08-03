def majority_element(nums: list[int]) -> int:
    if not nums:
        raise ValueError("nums must not be empty")

    candidate = None
    count = 0
    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    if nums.count(candidate) > len(nums) // 2:
        return candidate

    raise ValueError("no strict majority element exists")
