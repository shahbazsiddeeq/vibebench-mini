def two_sum(nums, target):
    """
    two_sum(nums, target) returns a tuple (i, j) with i < j such that
    nums[i] + nums[j] == target. When more than one valid pair exists, return the
    pair with the smallest second index j; among indices that could pair with that
    j, use the largest such i (that is, the index closest before j). Raises
    ValueError if no pair sums to target.
    """
    n = len(nums)
    best_pair = None

    # Iterate through all possible second indices j
    for j in range(1, n):
        # For a fixed j, we are looking for an i < j such that nums[i] + nums[j] == target
        # This means nums[i] = target - nums[j]
        complement = target - nums[j]

        # We need to find the largest i < j such that nums[i] == complement
        # Iterate backwards from j-1 down to 0 to find the largest such i
        found_i = -1
        for i in range(j - 1, -1, -1):
            if nums[i] == complement:
                found_i = i
                break

        if found_i != -1:
            # We found a valid pair (found_i, j)
            if best_pair is None:
                best_pair = (found_i, j)
            else:
                # If a best_pair already exists, we need to compare
                # The problem states: "return the pair with the smallest second index j"
                # Since we are iterating j in increasing order, the first valid pair
                # we find for a given j will automatically have the smallest j.
                # If we find another pair for the same j, we need to check the i.
                # "among indices that could pair with that j, use the largest such i"
                # Since we iterate i backwards, the first found_i for a given j is the largest.
                # Therefore, the first valid pair found for any j will be the correct one
                # according to the criteria.
                # We can break early once a pair is found, as subsequent j's will be larger.
                return best_pair

    if best_pair is None:
        raise ValueError("No pair sums to target")
    else:
        return best_pair
