import collections

def sliding_max(nums, k):
    """
    Calculates the maximum value in each sliding window of size k.

    Args:
        nums: A list of integers.
        k: The size of the sliding window.

    Returns:
        A list of maximum values for each window.

    Raises:
        ValueError: If k is less than or equal to 0, or if k is greater than
                    the length of nums.
    """
    n = len(nums)

    if k <= 0:
        raise ValueError("Window size k must be greater than 0.")
    if k > n:
        raise ValueError("Window size k cannot be greater than the length of nums.")

    if n == 0:
        return []
    if k == 1:
        return list(nums)

    result = []
    # Deque to store indices of elements in the current window in decreasing order of their values.
    # The front of the deque will always hold the index of the maximum element.
    dq = collections.deque()

    for i in range(n):
        # Remove elements from the front of the deque if they are outside the current window
        if dq and dq[0] <= i - k:
            dq.popleft()

        # Remove elements from the back of the deque if they are smaller than the current element
        # This maintains the decreasing order of values in the deque
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        # Add the current element's index to the back of the deque
        dq.append(i)

        # If the window has been fully formed, add the maximum element (at the front of the deque)
        # to the result list
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
