# src/solution.py

def lcs_length(s1: str, s2: str) -> int:
    # Validate inputs
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise ValueError("Both inputs must be strings.")
    
    # Initialize the lengths of the strings
    len_s1 = len(s1)
    len_s2 = len(s2)
    
    # Create a 2D array to store lengths of longest common subsequence
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]
    
    # Fill the dp array
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # The length of the longest common subsequence is in dp[len_s1][len_s2]
    return dp[len_s1][len_s2]
