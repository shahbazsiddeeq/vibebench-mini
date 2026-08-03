"""
src/solution.py

Minimum Coin Change solution.

Provides:
    min_coins(coins, amount) -> int

Security / robustness notes:
    - All inputs are validated strictly; invalid types or values raise
      ValueError (or TypeError for wrong types) with generic, non-leaking
      messages.
    - No use of eval/exec, no external I/O, no randomness needed.
    - Pure computation, deterministic, safe for untrusted numeric input.
"""

from typing import List


def min_coins(coins: List[int], amount: int) -> int:
    """
    Compute the minimum number of coins needed to make up `amount` using
    unlimited supply of denominations in `coins`.

    Args:
        coins: list of positive integer denominations.
        amount: non-negative integer target amount.

    Returns:
        Minimum number of coins needed, 0 if amount is 0, or -1 if the
        amount cannot be formed from the given denominations.

    Raises:
        ValueError: if any coin <= 0, or if amount < 0, or if inputs are
            not of the expected types.
    """
    # --- Input validation ---
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise ValueError("amount must be a non-negative integer")
    if amount < 0:
        raise ValueError("amount must be a non-negative integer")

    if not isinstance(coins, (list, tuple)):
        raise ValueError("coins must be a list of positive integers")

    validated_coins = []
    for c in coins:
        if not isinstance(c, int) or isinstance(c, bool):
            raise ValueError("each coin must be a positive integer")
        if c <= 0:
            raise ValueError("each coin must be a positive integer")
        validated_coins.append(c)

    if amount == 0:
        return 0

    if not validated_coins:
        return -1

    # --- Dynamic programming ---
    INF = amount + 1
    dp = [0] + [INF] * amount

    for i in range(1, amount + 1):
        best = INF
        for coin in validated_coins:
            if coin <= i:
                candidate = dp[i - coin] + 1
                if candidate < best:
                    best = candidate
        dp[i] = best

    return dp[amount] if dp[amount] != INF else -1
