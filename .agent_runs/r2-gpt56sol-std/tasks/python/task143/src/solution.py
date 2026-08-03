"""Quickselect implementation for finding the k-th largest integer."""


def kth_largest(nums: list[int], k: int) -> int:
    """Return the k-th largest value in *nums*, counting duplicates."""
    if not nums or k < 1 or k > len(nums):
        raise ValueError("k must be in the range 1..len(nums)")

    values = list(nums)
    target = len(values) - k
    left, right = 0, len(values) - 1

    while left <= right:
        pivot = values[(left + right) // 2]
        lower, current, upper = left, left, right

        # Three-way partition: values below, equal to, and above the pivot.
        while current <= upper:
            if values[current] < pivot:
                values[lower], values[current] = values[current], values[lower]
                lower += 1
                current += 1
            elif values[current] > pivot:
                values[current], values[upper] = values[upper], values[current]
                upper -= 1
            else:
                current += 1

        if target < lower:
            right = lower - 1
        elif target > upper:
            left = upper + 1
        else:
            return pivot

    raise RuntimeError("quickselect failed")
