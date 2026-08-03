from collections import deque

def sliding_max(nums, k):
    if k <= 0 or k > len(nums):
        raise ValueError("k must be greater than 0 and less than or equal to the length of nums")
    
    deq = deque()
    result = []

    for i in range(len(nums)):
        # Remove elements not within the sliding window
        if deq and deq[0] < i - k + 1:
            deq.popleft()
        
        # Remove elements smaller than the current element from the deque
        while deq and nums[deq[-1]] < nums[i]:
            deq.pop()
        
        # Add current element index to the deque
        deq.append(i)
        
        # Append the maximum for the current window to the result list
        if i >= k - 1:
            result.append(nums[deq[0]])
    
    return result
