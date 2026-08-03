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
    # Validate inputs
    if not isinstance(s1, str):
        raise TypeError("First argument must be a string")
    if not isinstance(s2, str):
        raise TypeError("Second argument must be a string")
    
    # Get lengths
    len1 = len(s1)
    len2 = len(s2)
    
    # Handle edge cases
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    
    # Create a matrix to store distances
    # dp[i][j] represents the edit distance between s1[0:i] and s2[0:j]
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    # Initialize base cases
    # Distance from empty string to s2[0:j] is j (all insertions)
    for j in range(len2 + 1):
        dp[0][j] = j
    
    # Distance from s1[0:i] to empty string is i (all deletions)
    for i in range(len1 + 1):
        dp[i][0] = i
    
    # Fill the matrix using dynamic programming
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            # If characters match, no operation needed
            if s1[i - 1] == s2[j - 1]:
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
    
    return dp[len1][len2]
