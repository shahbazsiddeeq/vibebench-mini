def lcs_length(s1: str, s2: str) -> int:
    """
    Calculates the length of the longest common subsequence of two strings.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The length of the longest common subsequence.
    """
    m = len(s1)
    n = len(s2)

    # Create a 2D array (list of lists) to store the lengths of LCS for subproblems.
    # dp[i][j] will store the length of LCS of s1[0...i-1] and s2[0...j-1].
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the dp table in a bottom-up manner
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
