def min_coins(coins: list[int], amount: int) -> int:
    """
    Calculates the minimum number of coins needed to make a given amount.

    Args:
        coins: A list of coin denominations, each available in unlimited supply.
               Must contain only positive integers.
        amount: The target amount to make. Must be a non-negative integer.

    Returns:
        The minimum number of coins (int) needed.
        Returns 0 if amount is 0.
        Returns -1 if the amount cannot be made from the given denominations.

    Raises:
        ValueError: If any coin denomination is less than or equal to 0,
                    or if the amount is negative.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    for coin in coins:
        if not isinstance(coin, int) or coin <= 0:
            raise ValueError("Coin denominations must be positive integers.")

    if amount == 0:
        return 0

    # Initialize dp array with infinity, dp[i] will store the minimum coins for amount i
    # dp[0] is 0 because 0 coins are needed for amount 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    # Iterate through each amount from 1 to 'amount'
    for i in range(1, amount + 1):
        # For each amount, iterate through available coin denominations
        for coin in coins:
            # If the current coin can be used to make the current amount 'i'
            # and a solution exists for the remaining amount (i - coin)
            if i - coin >= 0 and dp[i - coin] != float('inf'):
                # Update dp[i] with the minimum of its current value
                # and 1 (for the current coin) + dp[i - coin]
                dp[i] = min(dp[i], 1 + dp[i - coin])

    # If dp[amount] is still infinity, it means the amount cannot be made
    return dp[amount] if dp[amount] != float('inf') else -1
