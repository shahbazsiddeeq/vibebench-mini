def edit_distance(s1: str, s2: str) -> int:
    """
    Calculate the minimum edit distance (Levenshtein distance) between two strings.
    
    Operations allowed: insert, delete, replace (each costs 1).
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        The minimum number of edits needed to transform s1 into s2
    """
    m, n = len(s1), len(s2)
    
    # Create a DP table where dp[i][j] represents the edit distance
    # between s1[:i] and s2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases: transforming empty string to s2 requires insertions
    for j in range(n + 1):
        dp[0][j] = j
    
    # Base cases: transforming s1 to empty string requires deletions
    for i in range(m + 1):
        dp[i][0] = i
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Take minimum of three operations:
                # 1. Replace: dp[i-1][j-1] + 1
                # 2. Delete from s1: dp[i-1][j] + 1
                # 3. Insert into s1: dp[i][j-1] + 1
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # replace
                    dp[i - 1][j],      # delete
                    dp[i][j - 1]       # insert
                )
    
    return dp[m][n]
