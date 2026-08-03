# src/solution.py

def wildcard_match(pattern: str, text: str) -> bool:
    p_len = len(pattern)
    t_len = len(text)
    
    # dp[i][j] will be True if pattern[0..i-1] matches text[0..j-1]
    dp = [[False] * (t_len + 1) for _ in range(p_len + 1)]
    
    # Empty pattern matches empty text
    dp[0][0] = True
    
    # Handle patterns with '*' at the start
    for i in range(1, p_len + 1):
        if pattern[i - 1] == '*':
            dp[i][0] = dp[i - 1][0]
        else:
            break
    
    for i in range(1, p_len + 1):
        for j in range(1, t_len + 1):
            if pattern[i - 1] == '*':
                # '*' can match zero or more characters
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[i - 1] == '?' or pattern[i - 1] == text[j - 1]:
                # '?' matches any single character or exact match
                dp[i][j] = dp[i - 1][j - 1]
    
    return dp[p_len][t_len]
