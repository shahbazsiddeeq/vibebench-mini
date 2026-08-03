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

    for j in range(1, n):
        # For the current j, we are looking for an i < j such that nums[i] + nums[j] == target.
        # We need to find the largest such i.
        complement = target - nums[j]
        found_i = -1

        # Iterate backwards from j-1 to 0 to find the largest i
        for i in range(j - 1, -1, -1):
            if nums[i] == complement:
                found_i = i
                break

        if found_i != -1:
            # We found a valid pair (found_i, j)
            if best_pair is None:
                best_pair = (found_i, j)
            else:
                # If we already have a best_pair, we need to compare.
                # The problem states: "return the pair with the smallest second index j"
                # Since we are iterating j in increasing order, the first valid pair
                # we find for a given j will automatically have the smallest j.
                # If we find another pair for the same j (which shouldn't happen
                # if we break after finding the largest i), or if we find a pair
                # for a larger j, we only update if the new j is smaller.
                # However, the loop structure ensures that if we find a pair,
                # it's for the current j, which is the smallest j encountered so far
                # for which a pair exists.
                # The condition "among indices that could pair with that j, use the largest such i"
                # is handled by iterating i backwards.
                # So, once we find the first valid pair (found_i, j), it satisfies
                # both conditions for that specific j. Since we iterate j from smallest
                # to largest, the first pair found will have the smallest j.
                # Therefore, we can just return it.
                return (found_i, j)

    if best_pair is None:
        raise ValueError("No pair sums to target")
    else:
        # This part should ideally not be reached if the logic above is correct
        # and we return immediately. However, if we were to collect all valid
        # pairs and then filter, this would be relevant.
        # Given the problem statement, the first valid pair found by iterating
        # j from smallest to largest, and i from largest to smallest for that j,
        # is the correct answer.
        return best_pair
