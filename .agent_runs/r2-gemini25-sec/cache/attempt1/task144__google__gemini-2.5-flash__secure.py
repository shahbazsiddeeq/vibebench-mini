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
    if not isinstance(nums, list):
        raise TypeError("Input 'nums' must be a list.")
    if not nums:
        raise ValueError("Input list 'nums' cannot be empty.")

    # Input validation: Ensure all elements are integers
    for num in nums:
        if not isinstance(num, int):
            raise TypeError("All elements in 'nums' must be integers.")

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
    # After the first pass, 'candidate' is the only element that *could* be the majority element.
    # We must verify if it actually is.
    if candidate is None:  # Should not happen if nums is not empty, but as a safeguard
        raise ValueError("No majority element found.")

    actual_count = 0
    for num in nums:
        if num == candidate:
            actual_count += 1

    if actual_count > len(nums) // 2:
        return candidate
    else:
        raise ValueError("No strict majority element exists.")
