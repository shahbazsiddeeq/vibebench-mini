def edit_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings.

    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions or substitutions) required to change one word
    into the other.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The Levenshtein distance between s1 and s2.
    """
    len_s1 = len(s1)
    len_s2 = len(s2)

    # Create a 2D array (matrix) to store the distances
    # dp[i][j] will be the Levenshtein distance between s1[0...i-1] and s2[0...j-1]
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    # Initialize the first row and column
    # If s1 is empty, the distance to s2[0...j-1] is j (j insertions)
    for j in range(len_s2 + 1):
        dp[0][j] = j
    # If s2 is empty, the distance to s1[0...i-1] is i (i deletions)
    for i in range(len_s1 + 1):
        dp[i][0] = i

    # Fill the DP table
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters are the same, no cost for substitution
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Characters are different, consider three operations:
                # 1. Deletion: dp[i-1][j] + 1 (delete s1[i-1])
                # 2. Insertion: dp[i][j-1] + 1 (insert s2[j-1] into s1)
                # 3. Substitution: dp[i-1][j-1] + 1 (replace s1[i-1] with s2[j-1])
                dp[i][j] = 1 + min(dp[i - 1][j],      # Deletion
                                   dp[i][j - 1],      # Insertion
                                   dp[i - 1][j - 1])  # Substitution

    return dp[len_s1][len_s2]
