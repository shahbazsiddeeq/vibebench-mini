def min_coins(coins, amount):
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if any(coin <= 0 for coin in coins):
        raise ValueError("Coin denominations must be positive")

    if amount == 0:
        return 0

    # Initialize the dp array with a large number (amount + 1 is a safe upper bound)
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
