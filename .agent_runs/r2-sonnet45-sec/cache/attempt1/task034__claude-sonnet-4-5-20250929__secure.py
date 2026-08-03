def min_coins(coins, amount):
    """
    Returns the minimum number of coins needed to make the given amount.
    
    Args:
        coins: List of coin denominations (each available in unlimited supply)
        amount: Target amount to make
        
    Returns:
        int: Minimum number of coins needed, 0 if amount is 0, -1 if impossible
        
    Raises:
        ValueError: If any coin <= 0 or if amount < 0
    """
    # Validate amount
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    
    # Validate coins
    if coins:
        for coin in coins:
            if not isinstance(coin, (int, float)) or coin <= 0:
                raise ValueError("All coins must be positive")
    
    # Base case: amount is 0
    if amount == 0:
        return 0
    
    # If no coins available and amount > 0, impossible
    if not coins:
        return -1
    
    # Dynamic programming approach
    # dp[i] represents minimum coins needed to make amount i
    # Initialize with infinity (impossible) except dp[0] = 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # For each amount from 1 to target amount
    for i in range(1, amount + 1):
        # Try each coin denomination
        for coin in coins:
            # If this coin can be used (doesn't exceed current amount)
            if coin <= i:
                # Update minimum coins needed for amount i
                # Either keep current value or use (1 + coins needed for i-coin)
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    # If dp[amount] is still infinity, it's impossible
    return dp[amount] if dp[amount] != float('inf') else -1
