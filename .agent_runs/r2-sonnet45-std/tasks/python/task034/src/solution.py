def min_coins(coins, amount):
    # Validate inputs
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    
    for coin in coins:
        if coin <= 0:
            raise ValueError("Coin denominations must be positive")
    
    # Base case
    if amount == 0:
        return 0
    
    # If no coins available and amount > 0
    if not coins:
        return -1
    
    # Dynamic programming approach
    # dp[i] represents minimum coins needed to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # For each amount from 1 to target amount
    for i in range(1, amount + 1):
        # Try each coin denomination
        for coin in coins:
            if coin <= i:
                # If we can use this coin, update minimum
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    # If dp[amount] is still infinity, amount cannot be made
    return dp[amount] if dp[amount] != float('inf') else -1
