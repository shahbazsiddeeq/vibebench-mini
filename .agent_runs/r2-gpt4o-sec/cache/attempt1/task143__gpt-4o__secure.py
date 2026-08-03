import random
import secrets

def kth_largest(nums: list[int], k: int) -> int:
    if not nums:
        raise ValueError("The list cannot be empty.")
    if not (1 <= k <= len(nums)):
        raise ValueError("k must be in the range 1 to len(nums).")

    def partition(left, right, pivot_index):
        pivot_value = nums[pivot_index]
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        store_index = left
        for i in range(left, right):
            if nums[i] > pivot_value:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1
        nums[right], nums[store_index] = nums[store_index], nums[right]
        return store_index

    def quickselect(left, right, k_smallest):
        if left == right:
            return nums[left]

        pivot_index = secrets.randbelow(right - left + 1) + left
        pivot_index = partition(left, right, pivot_index)

        if k_smallest == pivot_index:
            return nums[k_smallest]
        elif k_smallest < pivot_index:
            return quickselect(left, pivot_index - 1, k_smallest)
        else:
            return quickselect(pivot_index + 1, right, k_smallest)

    return quickselect(0, len(nums) - 1, k - 1)
