def lcs_length(s1: str, s2: str) -> int:
    """
    Calculate the length of the longest common subsequence of two strings.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        The length of the longest common subsequence
    
    Raises:
        TypeError: If inputs are not strings
    """
    # Input validation
    if not isinstance(s1, str):
        raise TypeError("s1 must be a string")
    if not isinstance(s2, str):
        raise TypeError("s2 must be a string")
    
    # Handle empty strings
    if not s1 or not s2:
        return 0
    
    # Dynamic programming approach
    # Create a 2D table to store LCS lengths
    m, n = len(s1), len(s2)
    
    # Initialize DP table with zeros
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match: take diagonal value + 1
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters don't match: take maximum of left or top
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # The bottom-right cell contains the LCS length
    return dp[m][n]
