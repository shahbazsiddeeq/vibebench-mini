def two_sum(nums, target):
    """
    Finds two numbers in the list that sum up to the target.

    Args:
        nums (list): A list of integers.
        target (int): The target sum.

    Returns:
        tuple: A tuple (i, j) with i < j such that nums[i] + nums[j] == target.
               When more than one valid pair exists, returns the pair with the
               smallest second index j; among indices that could pair with that
               j, uses the largest such i (that is, the index closest before j).

    Raises:
        ValueError: If no pair sums to target, or if inputs are invalid.
    """
    if not isinstance(nums, list):
        raise ValueError("Input 'nums' must be a list.")
    if not all(isinstance(x, int) for x in nums):
        raise ValueError("All elements in 'nums' must be integers.")
    if not isinstance(target, int):
        raise ValueError("Input 'target' must be an integer.")
    if len(nums) < 2:
        raise ValueError("Input 'nums' must contain at least two elements.")

    best_pair = None
    min_j = float('inf')

    # Iterate through all possible second indices j
    for j in range(1, len(nums)):
        complement = target - nums[j]
        found_i = -1

        # Search for the largest i < j such that nums[i] == complement
        for i in range(j - 1, -1, -1):
            if nums[i] == complement:
                found_i = i
                break

        if found_i != -1:
            # If this j is smaller than the current minimum j, update
            if j < min_j:
                min_j = j
                best_pair = (found_i, j)
            # If this j is equal to the current minimum j, and this i is larger, update
            elif j == min_j and found_i > best_pair[0]:
                best_pair = (found_i, j)

    if best_pair is None:
        raise ValueError("No two sum solution")

    return best_pair
