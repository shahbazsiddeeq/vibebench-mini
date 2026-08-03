def min_coins(coins, amount):
    if amount < 0:
        raise ValueError("amount must be non-negative")
    for c in coins:
        if c <= 0:
            raise ValueError("coins must be positive")

    if amount == 0:
        return 0

    INF = float('inf')
    dp = [0] + [INF] * amount

    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1

    return dp[amount] if dp[amount] != INF else -1
