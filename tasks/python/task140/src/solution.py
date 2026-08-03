from __future__ import annotations


def max_subarray(nums: list[int]) -> tuple[int, int, int]:
    """Return (max_sum, start, end) of the max-sum contiguous subarray.

    Tie-break: smallest start index, then smallest end index.
    """
    if not nums:
        raise ValueError("nums must be non-empty")

    best_sum: int | None = None
    best_start = 0
    best_end = 0

    cur_sum = 0
    cur_start = 0

    for i, x in enumerate(nums):
        if cur_sum < 0:
            # Restarting yields a strictly larger sum ending at i.
            cur_sum = x
            cur_start = i
        else:
            # Extending keeps the earliest possible start (preferred on ties).
            cur_sum += x

        if best_sum is None or cur_sum > best_sum:
            best_sum = cur_sum
            best_start = cur_start
            best_end = i

    assert best_sum is not None
    return (best_sum, best_start, best_end)
