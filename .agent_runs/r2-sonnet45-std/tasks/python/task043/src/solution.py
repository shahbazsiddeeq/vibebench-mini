def edit_distance(s1, s2):
    """
    Calculate the minimum edit distance (Levenshtein distance) between two strings.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Minimum number of edits (insert/delete/replace) needed to transform s1 into s2
    """
    m, n = len(s1), len(s2)
    
    # Create a DP table with dimensions (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    # Converting empty string to s2[:j] requires j insertions
    for j in range(n + 1):
        dp[0][j] = j
    
    # Converting s1[:i] to empty string requires i deletions
    for i in range(m + 1):
        dp[i][0] = i
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match, no edit needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Take minimum of:
                # 1. Replace: dp[i-1][j-1] + 1
                # 2. Delete from s1: dp[i-1][j] + 1
                # 3. Insert into s1: dp[i][j-1] + 1
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # Replace
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1]       # Insert
                )
    
    return dp[m][n]
