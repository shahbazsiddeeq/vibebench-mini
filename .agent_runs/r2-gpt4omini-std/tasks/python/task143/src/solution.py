# src/solution.py

import random

def kth_largest(nums: list[int], k: int) -> int:
    if not nums:
        raise ValueError("The input list is empty.")
    if k < 1 or k > len(nums):
        raise ValueError("k must be in the range 1 to len(nums).")

    def quickselect(left: int, right: int, index: int) -> int:
        pivot = nums[right]
        partition_index = left
        
        for i in range(left, right):
            if nums[i] > pivot:  # We want the k-th largest, so we use '>'
                nums[i], nums[partition_index] = nums[partition_index], nums[i]
                partition_index += 1
        
        nums[partition_index], nums[right] = nums[right], nums[partition_index]
        
        if partition_index == index:
            return nums[partition_index]
        elif partition_index < index:
            return quickselect(partition_index + 1, right, index)
        else:
            return quickselect(left, partition_index - 1, index)

    return quickselect(0, len(nums) - 1, k - 1)
