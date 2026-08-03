# src/solution.py

def min_coins(coins, amount):
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    if any(coin <= 0 for coin in coins):
        raise ValueError("All coins must be greater than zero.")
    
    if amount == 0:
        return 0
    if not coins:
        return -1

    # Initialize a list to store the minimum coins needed for each amount
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins are needed to make amount 0

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
