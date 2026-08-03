"""Glob-style wildcard matching (fully anchored) using '*' and '?'."""


def wildcard_match(pattern: str, text: str) -> bool:
    """Return True if `pattern` matches the entirety of `text`.

    '*' matches any run of zero or more characters.
    '?' matches exactly one character (one code point).
    All other characters must match exactly.
    """
    m, n = len(pattern), len(text)

    # dp[j] represents whether pattern[:i] matches text[:j] for current i
    dp = [False] * (n + 1)
    dp[0] = True

    for j in range(1, n + 1):
        dp[j] = False  # empty pattern only matches empty text

    for i in range(1, m + 1):
        p_char = pattern[i - 1]
        new_dp = [False] * (n + 1)
        if p_char == '*':
            # '*' can match empty string: inherits dp[i-1][0]
            new_dp[0] = dp[0]
            for j in range(1, n + 1):
                new_dp[j] = new_dp[j - 1] or dp[j]
        else:
            new_dp[0] = False
            for j in range(1, n + 1):
                if p_char == '?' or p_char == text[j - 1]:
                    new_dp[j] = dp[j - 1]
                else:
                    new_dp[j] = False
        dp = new_dp

    return dp[n]
