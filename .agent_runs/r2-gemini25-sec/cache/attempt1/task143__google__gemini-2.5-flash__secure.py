import secrets

def kth_largest(nums: list[int], k: int) -> int:
    """
    Returns the k-th largest value in nums using quickselect where k=1 is the maximum.
    Duplicates are counted by position so kth_largest([3,3,3], 2) == 3.

    Args:
        nums: A list of integers.
        k: The k-th largest element to find (1-indexed).

    Returns:
        The k-th largest integer in the list.

    Raises:
        ValueError: If nums is empty or if k is not in the range 1..len(nums).
    """
    if not isinstance(nums, list):
        raise TypeError("nums must be a list.")
    if not all(isinstance(x, int) for x in nums):
        raise TypeError("All elements in nums must be integers.")
    if not nums:
        raise ValueError("nums cannot be empty.")
    if not isinstance(k, int):
        raise TypeError("k must be an integer.")
    if not (1 <= k <= len(nums)):
        raise ValueError(f"k must be in the range 1..{len(nums)}.")

    # Quickselect works by finding the (n-k)-th smallest element.
    # If k=1 (largest), we need the (n-1)-th smallest element (0-indexed).
    # If k=len(nums) (smallest), we need the (n-len(nums))-th = 0th smallest element.
    # So, we are looking for the element at index `len(nums) - k` if the list were sorted ascending.
    target_index = len(nums) - k

    # Create a mutable copy to avoid modifying the original list
    arr = list(nums)

    return _quickselect(arr, 0, len(arr) - 1, target_index)

def _quickselect(arr: list[int], left: int, right: int, target_index: int) -> int:
    """
    Helper function for quickselect algorithm.
    Finds the element at target_index in the sorted version of arr[left:right+1].
    """
    if left == right:
        return arr[left]

    pivot_index = _partition(arr, left, right)

    if pivot_index == target_index:
        return arr[pivot_index]
    elif pivot_index < target_index:
        return _quickselect(arr, pivot_index + 1, right, target_index)
    else:  # pivot_index > target_index
        return _quickselect(arr, left, pivot_index - 1, target_index)

def _partition(arr: list[int], left: int, right: int) -> int:
    """
    Partitions the array arr[left:right+1] around a randomly chosen pivot.
    Returns the final index of the pivot element.
    """
    # Choose a random pivot to ensure average O(N) performance and
    # protect against worst-case O(N^2) for already sorted/reverse-sorted arrays.
    pivot_idx = secrets.randbelow(right - left + 1) + left
    pivot_value = arr[pivot_idx]

    # Move pivot to the end
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]

    store_index = left
    for i in range(left, right):
        if arr[i] < pivot_value:
            arr[store_index], arr[i] = arr[i], arr[store_index]
            store_index += 1

    # Move pivot to its final sorted position
    arr[right], arr[store_index] = arr[store_index], arr[right]
    return store_index
