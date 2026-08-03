import random


def kth_largest(nums: list[int], k: int) -> int:
    if not nums:
        raise ValueError("nums must not be empty")
    n = len(nums)
    if k < 1 or k > n:
        raise ValueError(f"k must be in range 1..{n}")

    arr = list(nums)
    target = k - 1  # index in descending sorted order

    def partition(left: int, right: int, pivot_index: int) -> int:
        pivot_value = arr[pivot_index]
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
        store_index = left
        for i in range(left, right):
            if arr[i] > pivot_value:  # descending order
                arr[store_index], arr[i] = arr[i], arr[store_index]
                store_index += 1
        arr[right], arr[store_index] = arr[store_index], arr[right]
        return store_index

    left, right = 0, n - 1
    while left < right:
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        if pivot_index == target:
            break
        elif pivot_index < target:
            left = pivot_index + 1
        else:
            right = pivot_index - 1

    return arr[target]
