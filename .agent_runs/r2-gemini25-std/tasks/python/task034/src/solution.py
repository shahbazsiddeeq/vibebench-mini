def min_coins(coins, amount):
    """
    Calculates the minimum number of coins needed to make a given amount.

    Args:
        coins: A list of coin denominations, each available in unlimited supply.
               Must contain only positive integers.
        amount: The target amount to make. Must be a non-negative integer.

    Returns:
        The minimum number of coins (int) needed to make the amount.
        Returns 0 if amount is 0.
        Returns -1 if the amount cannot be made from the given denominations.

    Raises:
        ValueError: If any coin denomination is less than or equal to 0,
                    or if the amount is negative.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    if any(coin <= 0 for coin in coins):
        raise ValueError("Coin denominations must be positive integers.")

    if amount == 0:
        return 0

    # Initialize dp array where dp[i] will store the minimum coins needed for amount i
    # Initialize with amount + 1, which is effectively infinity for this problem
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0  # 0 coins needed for amount 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != amount + 1 else -1
