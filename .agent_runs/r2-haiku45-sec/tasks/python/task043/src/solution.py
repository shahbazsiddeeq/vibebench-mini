def edit_distance(s1: str, s2: str) -> int:
    """
    Calculate the minimum edit distance (Levenshtein distance) between two strings.
    
    The edit distance is the minimum number of single-character edits (insertions,
    deletions, or substitutions) required to change one string into another.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        The minimum edit distance between s1 and s2
    
    Raises:
        TypeError: If inputs are not strings
    """
    # Input validation
    if not isinstance(s1, str):
        raise TypeError("s1 must be a string")
    if not isinstance(s2, str):
        raise TypeError("s2 must be a string")
    
    # Get lengths
    len1 = len(s1)
    len2 = len(s2)
    
    # Create a DP table with dimensions (len1 + 1) x (len2 + 1)
    # dp[i][j] represents the edit distance between s1[:i] and s2[:j]
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    # Initialize base cases
    # Distance from empty string to s2[:j] is j (j insertions)
    for j in range(len2 + 1):
        dp[0][j] = j
    
    # Distance from s1[:i] to empty string is i (i deletions)
    for i in range(len1 + 1):
        dp[i][0] = i
    
    # Fill the DP table
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Characters don't match, take minimum of:
                # 1. Replace: dp[i-1][j-1] + 1
                # 2. Delete from s1: dp[i-1][j] + 1
                # 3. Insert into s1: dp[i][j-1] + 1
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # replace
                    dp[i - 1][j],      # delete
                    dp[i][j - 1]       # insert
                )
    
    return dp[len1][len2]
