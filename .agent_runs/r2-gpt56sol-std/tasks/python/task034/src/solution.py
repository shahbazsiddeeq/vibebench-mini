"""Minimum coin change implementation."""

from typing import Sequence


def min_coins(coins: Sequence[int], amount: int) -> int:
    """Return the minimum number of coins needed to make ``amount``.

    Each denomination may be used an unlimited number of times. Returns -1
    when the amount cannot be made.

    Raises:
        ValueError: If ``amount`` is negative or any denomination is not
            positive.
    """
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if any(coin <= 0 for coin in coins):
        raise ValueError("coin denominations must be positive")
    if amount == 0:
        return 0

    unreachable = amount + 1
    minimum = [0] + [unreachable] * amount

    for coin in coins:
        for current in range(coin, amount + 1):
            minimum[current] = min(
                minimum[current],
                minimum[current - coin] + 1,
            )

    return -1 if minimum[amount] == unreachable else minimum[amount]
