from collections import deque

def sliding_max(nums, k):
    if not isinstance(nums, list) or not all(isinstance(x, (int, float)) for x in nums):
        raise ValueError("nums must be a list of numbers.")
    if not isinstance(k, int) or k <= 0 or k > len(nums):
        raise ValueError("k must be a positive integer less than or equal to the length of nums.")
    
    deq = deque()
    max_values = []

    for i, num in enumerate(nums):
        # Remove elements not within the sliding window
        if deq and deq[0] < i - k + 1:
            deq.popleft()
        
        # Remove elements smaller than the current element from the deque
        while deq and nums[deq[-1]] < num:
            deq.pop()
        
        # Add current element index to the deque
        deq.append(i)
        
        # Append the maximum for the current window to the result list
        if i >= k - 1:
            max_values.append(nums[deq[0]])
    
    return max_values
