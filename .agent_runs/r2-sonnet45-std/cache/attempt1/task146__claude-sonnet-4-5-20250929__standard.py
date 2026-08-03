def wildcard_match(pattern: str, text: str) -> bool:
    """
    Match pattern against text with wildcards.
    '*' matches zero or more characters.
    '?' matches exactly one character.
    Must match the entire text (fully anchored).
    """
    m, n = len(pattern), len(text)
    
    # dp[i][j] = True if pattern[0:i] matches text[0:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    
    # Empty pattern matches empty text
    dp[0][0] = True
    
    # Handle patterns that start with '*' - they can match empty text
    for i in range(1, m + 1):
        if pattern[i - 1] == '*':
            dp[i][0] = dp[i - 1][0]
        else:
            break
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[i - 1] == '*':
                # '*' can match zero characters (dp[i-1][j])
                # or one or more characters (dp[i][j-1])
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[i - 1] == '?':
                # '?' matches exactly one character
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Literal character must match exactly
                dp[i][j] = dp[i - 1][j - 1] and pattern[i - 1] == text[j - 1]
    
    return dp[m][n]
