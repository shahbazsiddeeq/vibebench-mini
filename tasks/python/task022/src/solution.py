from __future__ import annotations


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    seen: dict[int, int] = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i
    raise ValueError("no two-sum solution found")
