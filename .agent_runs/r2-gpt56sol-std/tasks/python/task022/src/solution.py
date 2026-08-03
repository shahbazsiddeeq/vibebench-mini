def two_sum(nums, target):
    """Return the preferred pair of indices whose values sum to target.

    The pair with the smallest second index is selected. For that second
    index, the largest valid preceding index is selected.

    Raises:
        ValueError: If no pair sums to target.
    """
    latest_index = {}

    for j, value in enumerate(nums):
        complement = target - value
        if complement in latest_index:
            return latest_index[complement], j
        latest_index[value] = j

    raise ValueError("no two numbers sum to target")
