def wildcard_match(pattern: str, text: str) -> bool:
    """
    Reports whether pattern matches the ENTIRE text (fully anchored).

    Two wildcards are recognized in pattern:
    '*' matches any run of zero or more characters.
    '?' matches exactly one character.

    Every other character must match the corresponding text character exactly.
    Matching is case-sensitive and operates on Unicode code points.

    Args:
        pattern: The wildcard pattern string.
        text: The text string to match against.

    Returns:
        True if the pattern matches the entire text, False otherwise.
    """
    p_len = len(pattern)
    t_len = len(text)

    # dp[i][j] will be True if pattern[:i] matches text[:j]
    dp = [[False] * (t_len + 1) for _ in range(p_len + 1)]

    # Base case: empty pattern matches empty text
    dp[0][0] = True

    # Handle patterns with leading '*'
    for i in range(1, p_len + 1):
        if pattern[i - 1] == '*':
            dp[i][0] = dp[i - 1][0]

    # Fill the DP table
    for i in range(1, p_len + 1):
        for j in range(1, t_len + 1):
            if pattern[i - 1] == '*':
                # '*' can match zero characters (dp[i-1][j])
                # or one or more characters (dp[i][j-1])
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[i - 1] == '?':
                # '?' matches exactly one character
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Literal character match
                dp[i][j] = (pattern[i - 1] == text[j - 1]) and dp[i - 1][j - 1]

    return dp[p_len][t_len]
