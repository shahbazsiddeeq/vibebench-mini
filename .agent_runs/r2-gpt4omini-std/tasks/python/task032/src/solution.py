# src/solution.py

from collections import deque

def sliding_max(nums, k):
    if k <= 0 or k > len(nums):
        raise ValueError("k must be greater than 0 and less than or equal to the length of nums.")
    
    result = []
    dq = deque()  # Deque to store indices of useful elements for the current window

    for i in range(len(nums)):
        # Remove elements not in the current window
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove elements from the deque that are less than the current element
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        # Add the current element's index to the deque
        dq.append(i)
        
        # The first k-1 windows are not full, so we start adding results after that
        if i >= k - 1:
            result.append(nums[dq[0]])  # The front of the deque is the maximum for the current window

    return result
