# src/solution.py

from collections import deque

def sliding_max(nums, k):
    if not isinstance(nums, list) or not all(isinstance(n, (int, float)) for n in nums):
        raise ValueError("nums must be a list of numbers.")
    if not isinstance(k, int) or k <= 0 or k > len(nums):
        raise ValueError("k must be a positive integer and less than or equal to the length of nums.")
    
    result = []
    deq = deque()  # Store indices of useful elements for the current window

    for i in range(len(nums)):
        # Remove indices that are out of the current window
        if deq and deq[0] < i - k + 1:
            deq.popleft()
        
        # Remove elements from the deque that are less than the current element
        while deq and nums[deq[-1]] < nums[i]:
            deq.pop()
        
        # Add the current element's index to the deque
        deq.append(i)
        
        # The first k-1 windows will not be complete
        if i >= k - 1:
            result.append(nums[deq[0]])  # The front of the deque is the largest element for the current window

    return result
