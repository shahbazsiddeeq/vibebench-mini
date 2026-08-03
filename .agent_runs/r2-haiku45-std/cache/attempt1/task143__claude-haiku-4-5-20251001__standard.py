import random


def kth_largest(nums: list[int], k: int) -> int:
    """
    Returns the k-th largest value in nums using quickselect.
    k=1 is the maximum.
    Duplicates are counted by position.
    Raises ValueError if nums is empty or if k is not in range 1..len(nums).
    """
    if not nums:
        raise ValueError("nums is empty")
    
    if k < 1 or k > len(nums):
        raise ValueError(f"k must be in range 1..{len(nums)}")
    
    # Convert k (1-indexed, largest first) to 0-indexed position from the left
    # k=1 means largest, which is at index 0 when sorted descending
    # This is equivalent to finding the element at index (k-1) in descending order
    # Or equivalently, finding the element at index (len(nums) - k) in ascending order
    target_index = len(nums) - k
    
    def quickselect(left: int, right: int, target: int) -> int:
        if left == right:
            return nums[left]
        
        # Partition around a pivot
        pivot_index = partition(left, right)
        
        if target == pivot_index:
            return nums[target]
        elif target < pivot_index:
            return quickselect(left, pivot_index - 1, target)
        else:
            return quickselect(pivot_index + 1, right, target)
    
    def partition(left: int, right: int) -> int:
        # Choose a random pivot to avoid worst-case O(n^2)
        random_index = random.randint(left, right)
        nums[random_index], nums[right] = nums[right], nums[random_index]
        
        pivot_value = nums[right]
        i = left
        
        for j in range(left, right):
            if nums[j] < pivot_value:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        
        nums[i], nums[right] = nums[right], nums[i]
        return i
    
    return quickselect(0, len(nums) - 1, target_index)
