def kth_largest(nums: list[int], k: int) -> int:
    """
    Returns the k-th largest value in nums using quickselect where k=1 is the maximum.
    Duplicates are counted by position so kth_largest([3,3,3], 2) == 3.
    Raises ValueError if nums is empty or if k is not in the range 1..len(nums).

    Example:
    kth_largest([3,2,1,5,6,4], 2) -> 5
    """
    if not nums:
        raise ValueError("Input list 'nums' cannot be empty.")
    if not (1 <= k <= len(nums)):
        raise ValueError(f"k must be in the range 1..len(nums), but got k={k} for list of length {len(nums)}.")

    # Quickselect algorithm
    # We are looking for the k-th largest element, which is equivalent to
    # the (n - k)-th smallest element in a 0-indexed array.
    target_index = len(nums) - k

    def _quickselect(arr, left, right, target_idx):
        if left == right:
            return arr[left]

        pivot_index = _partition(arr, left, right)

        if target_idx == pivot_index:
            return arr[target_idx]
        elif target_idx < pivot_index:
            return _quickselect(arr, left, pivot_index - 1, target_idx)
        else:
            return _quickselect(arr, pivot_index + 1, right, target_idx)

    def _partition(arr, left, right):
        # Using the rightmost element as the pivot
        pivot = arr[right]
        i = left  # Pointer for elements smaller than pivot

        for j in range(left, right):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[right] = arr[right], arr[i]  # Place pivot in its correct position
        return i

    # Create a copy to avoid modifying the original list if it's not desired
    # Although the problem description doesn't explicitly forbid modification,
    # it's good practice for functions that return a value based on input.
    # However, quickselect is often implemented in-place for efficiency.
    # For this problem, an in-place modification is acceptable as per typical quickselect usage.
    return _quickselect(nums, 0, len(nums) - 1, target_index)
