def min_coins(coins, amount):
    """
    Returns the minimum number of coins needed to make amount.
    
    Args:
        coins: List of coin denominations (each available in unlimited supply)
        amount: Target amount to make
        
    Returns:
        Minimum number of coins needed, 0 if amount is 0, -1 if impossible
        
    Raises:
        ValueError: If any coin <= 0 or if amount < 0
    """
    # Validate inputs
    if amount < 0:
        raise ValueError("amount cannot be negative")
    
    for coin in coins:
        if coin <= 0:
            raise ValueError("coin denominations must be positive")
    
    # Base case: amount is 0
    if amount == 0:
        return 0
    
    # If no coins available and amount > 0, impossible
    if not coins:
        return -1
    
    # Dynamic programming approach
    # dp[i] represents minimum coins needed to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    # If dp[amount] is still infinity, it's impossible
    return dp[amount] if dp[amount] != float('inf') else -1
