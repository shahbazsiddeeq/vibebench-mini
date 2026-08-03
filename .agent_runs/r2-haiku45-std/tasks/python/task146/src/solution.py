def wildcard_match(pattern: str, text: str) -> bool:
    """
    Match a wildcard pattern against text.
    
    '*' matches zero or more characters
    '?' matches exactly one character
    All other characters must match exactly
    
    The match must be anchored (match the entire text).
    """
    # Dynamic programming approach
    # dp[i][j] = True if pattern[:i] matches text[:j]
    
    m = len(pattern)
    n = len(text)
    
    # Create DP table
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    # Empty pattern matches empty text
    dp[0][0] = True
    
    # Handle patterns like *, **, ***, etc. that can match empty text
    for i in range(1, m + 1):
        if pattern[i - 1] == '*':
            dp[i][0] = dp[i - 1][0]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[i - 1] == '*':
                # '*' can match zero characters (dp[i-1][j])
                # or one or more characters (dp[i][j-1])
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[i - 1] == '?' or pattern[i - 1] == text[j - 1]:
                # '?' matches any single character
                # or literal character must match
                dp[i][j] = dp[i - 1][j - 1]
    
    return dp[m][n]
