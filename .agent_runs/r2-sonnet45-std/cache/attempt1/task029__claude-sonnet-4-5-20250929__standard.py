def lcs_length(s1, s2):
    """
    Returns the length of the longest common subsequence of strings s1 and s2.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Length of the longest common subsequence
    """
    m, n = len(s1), len(s2)
    
    # Create a DP table with (m+1) x (n+1) dimensions
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match, extend the LCS
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters don't match, take the maximum
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]
