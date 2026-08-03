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
        text: The text string to match against the pattern.

    Returns:
        True if the pattern matches the entire text, False otherwise.
    """
    if not isinstance(pattern, str) or not isinstance(text, str):
        # While the problem statement says "never raise for ordinary str inputs",
        # it's good practice to validate types for robustness, especially if
        # this function might be called with non-string types in a larger system.
        # For this specific problem, we'll assume inputs are always strings
        # as per the prompt's "ordinary str inputs" and return False for invalid types.
        return False

    # Dynamic programming approach
    # dp[i][j] will be True if pattern[:i] matches text[:j]
    n = len(pattern)
    m = len(text)

    dp = [[False] * (m + 1) for _ in range(n + 1)]

    # Base case: empty pattern matches empty text
    dp[0][0] = True

    # Handle patterns with leading '*'
    # '*' can match an empty string, so dp[i][0] can be true if pattern[:i] is all '*'
    for i in range(1, n + 1):
        if pattern[i - 1] == '*':
            dp[i][0] = dp[i - 1][0]

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
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

    return dp[n][m]
