def majority_element(nums: list[int]) -> int:
    """
    Finds the majority element in a list of integers using the Boyer-Moore voting algorithm
    followed by a verification pass.

    A majority element is an element that appears strictly more than len(nums) // 2 times.

    Args:
        nums: A list of integers.

    Returns:
        The majority element.

    Raises:
        ValueError: If nums is empty or if no strict majority element exists.
    """
    if not nums:
        raise ValueError("Input list cannot be empty.")

    # Boyer-Moore Voting Algorithm
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

    # Verification Pass
    # After the first pass, 'candidate' is the only element that could
    # be the majority element. We need to verify if it indeed is.
    if candidate is not None:
        actual_count = nums.count(candidate)
        if actual_count > len(nums) // 2:
            return candidate

    raise ValueError("No strict majority element found.")
