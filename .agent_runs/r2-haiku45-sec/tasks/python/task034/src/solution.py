"""
Coin Change (Minimum Coins) - Dynamic Programming Solution

This module provides a function to find the minimum number of coins needed
to make a given amount from a list of coin denominations.
"""

from typing import List


def min_coins(coins: List[int], amount: int) -> int:
    """
    Returns the minimum number of coins needed to make the given amount.
    
    Args:
        coins: A list of coin denominations (positive integers)
        amount: The target amount (non-negative integer)
    
    Returns:
        The minimum number of coins needed to make the amount.
        Returns 0 if amount is 0.
        Returns -1 if the amount cannot be made from the given denominations.
    
    Raises:
        ValueError: If any coin is <= 0 or if amount < 0
    
    Example:
        >>> min_coins([1, 5, 6, 9], 11)
        2
    """
    # Input validation
    if amount < 0:
        raise ValueError("amount must be non-negative")
    
    # Validate coins - check for non-positive values
    for coin in coins:
        if not isinstance(coin, int) or coin <= 0:
            raise ValueError("all coins must be positive integers")
    
    # Base case: amount is 0
    if amount == 0:
        return 0
    
    # Base case: no coins available but amount > 0
    if not coins:
        return -1
    
    # Dynamic programming approach
    # dp[i] represents the minimum number of coins needed to make amount i
    # Initialize with amount + 1 (impossible value, larger than any valid answer)
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed to make amount 0
    
    # Fill the dp table
    for current_amount in range(1, amount + 1):
        for coin in coins:
            # If the coin is not larger than current amount
            if coin <= current_amount:
                # Try using this coin and check if it gives a better solution
                dp[current_amount] = min(dp[current_amount], dp[current_amount - coin] + 1)
    
    # If dp[amount] is still amount + 1, it means the amount cannot be made
    if dp[amount] > amount:
        return -1
    
    return dp[amount]
