def kth_largest(nums: list[int], k: int) -> int:
    """
    Returns the k-th largest value in nums using quickselect.
    k=1 is the maximum. Duplicates are counted by position.
    
    Args:
        nums: List of integers
        k: Position (1-indexed) of the largest element to find
        
    Returns:
        The k-th largest element
        
    Raises:
        ValueError: If nums is empty or k is not in range 1..len(nums)
    """
    if not nums:
        raise ValueError("nums cannot be empty")
    if k < 1 or k > len(nums):
        raise ValueError(f"k must be in range 1..{len(nums)}")
    
    # Work with a copy to avoid mutating the input
    arr = nums.copy()
    
    # We want the k-th largest, which is at index k-1 in descending order
    # Or equivalently, at index len(arr) - k in ascending order
    target_index = len(arr) - k
    
    def quickselect(left: int, right: int) -> int:
        """
        Partition and recursively find the element at target_index.
        """
        if left == right:
            return arr[left]
        
        # Choose pivot (using middle element for better average performance)
        pivot_index = (left + right) // 2
        pivot_value = arr[pivot_index]
        
        # Move pivot to the end
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
        
        # Partition: elements less than pivot go to the left
        store_index = left
        for i in range(left, right):
            if arr[i] < pivot_value:
                arr[i], arr[store_index] = arr[store_index], arr[i]
                store_index += 1
        
        # Move pivot to its final position
        arr[store_index], arr[right] = arr[right], arr[store_index]
        
        # Recurse on the appropriate partition
        if target_index == store_index:
            return arr[store_index]
        elif target_index < store_index:
            return quickselect(left, store_index - 1)
        else:
            return quickselect(store_index + 1, right)
    
    return quickselect(0, len(arr) - 1)
