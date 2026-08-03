from __future__ import annotations


def min_coins(coins: list[int], amount: int) -> int:
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if any(c <= 0 for c in coins):
        raise ValueError("all coin values must be positive")
    if amount == 0:
        return 0
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return int(dp[amount]) if dp[amount] != float("inf") else -1
