"""Minimum coin change implementation."""

from math import gcd
from typing import Iterable


def min_coins(coins: Iterable[int], amount: int) -> int:
    """Return the minimum number of reusable coins needed to make ``amount``.

    Returns -1 when the amount cannot be formed. Invalid denominations and
    negative amounts raise ValueError.
    """
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("amount must be an integer")
    if amount < 0:
        raise ValueError("amount must be non-negative")

    if isinstance(coins, (str, bytes)):
        raise ValueError("coins must be an iterable of positive integers")

    try:
        denominations = list(coins)
    except TypeError as exc:
        raise ValueError("coins must be an iterable of positive integers") from exc

    for coin in denominations:
        if isinstance(coin, bool) or not isinstance(coin, int):
            raise ValueError("coin denominations must be integers")
        if coin <= 0:
            raise ValueError("coin denominations must be positive")

    if amount == 0:
        return 0

    usable = sorted({coin for coin in denominations if coin <= amount})
    if not usable:
        return -1
    if amount in usable:
        return 1

    common_divisor = 0
    for coin in usable:
        common_divisor = gcd(common_divisor, coin)

    if amount % common_divisor:
        return -1

    if common_divisor > 1:
        amount //= common_divisor
        usable = [coin // common_divisor for coin in usable]

    unreachable = amount + 1
    minimum = [unreachable] * (amount + 1)
    minimum[0] = 0

    for coin in usable:
        for subtotal in range(coin, amount + 1):
            candidate = minimum[subtotal - coin] + 1
            if candidate < minimum[subtotal]:
                minimum[subtotal] = candidate

    return -1 if minimum[amount] == unreachable else minimum[amount]
