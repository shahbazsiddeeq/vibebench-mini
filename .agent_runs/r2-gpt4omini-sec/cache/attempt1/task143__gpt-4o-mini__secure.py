# src/solution.py

import random
import secrets

def kth_largest(nums: list[int], k: int) -> int:
    if not nums:
        raise ValueError("The input list cannot be empty.")
    if k < 1 or k > len(nums):
        raise ValueError("k must be in the range 1 to len(nums).")

    def quickselect(left: int, right: int, index: int) -> int:
        if left == right:
            return nums[left]

        pivot_index = secrets.randbelow(right - left + 1) + left
        pivot_value = nums[pivot_index]

        # Move pivot to the end
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        store_index = left

        for i in range(left, right):
            if nums[i] > pivot_value:  # We want the k-th largest
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1

        # Move pivot to its final place
        nums[store_index], nums[right] = nums[right], nums[store_index]

        if index == store_index:
            return nums[index]
        elif index < store_index:
            return quickselect(left, store_index - 1, index)
        else:
            return quickselect(store_index + 1, right, index)

    return quickselect(0, len(nums) - 1, k - 1)
