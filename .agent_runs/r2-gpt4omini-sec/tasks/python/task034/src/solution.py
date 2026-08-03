# src/solution.py

def min_coins(coins, amount):
    # Validate inputs
    if not isinstance(coins, list) or not all(isinstance(coin, int) for coin in coins):
        raise ValueError("Coins must be a list of integers.")
    if any(coin <= 0 for coin in coins):
        raise ValueError("All coin denominations must be greater than zero.")
    if not isinstance(amount, int):
        raise ValueError("Amount must be an integer.")
    if amount < 0:
        raise ValueError("Amount must be non-negative.")

    # If amount is 0, no coins are needed
    if amount == 0:
        return 0

    # Initialize a list to store the minimum coins needed for each amount
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins are needed to make amount 0

    # Compute the minimum coins needed for each amount from 1 to the target amount
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    # If dp[amount] is still infinity, it means we cannot make that amount
    return dp[amount] if dp[amount] != float('inf') else -1
