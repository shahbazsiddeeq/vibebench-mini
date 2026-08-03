def edit_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein edit distance between two strings.

    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions, or substitutions) required to change one word
    into the other.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The Levenshtein distance between s1 and s2.

    Raises:
        TypeError: If s1 or s2 are not strings.
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Both s1 and s2 must be strings.")

    len_s1 = len(s1)
    len_s2 = len(s2)

    # Create a 2D array (matrix) to store the distances
    # dp[i][j] will be the Levenshtein distance between the first i characters of s1
    # and the first j characters of s2.
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    # Initialize the first row and column
    # If s1 is empty, the distance to s2 is the length of s2 (all insertions)
    for i in range(len_s1 + 1):
        dp[i][0] = i
    # If s2 is empty, the distance to s1 is the length of s1 (all deletions)
    for j in range(len_s2 + 1):
        dp[0][j] = j

    # Fill the DP table
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Deletion
                dp[i][j - 1] + 1,      # Insertion
                dp[i - 1][j - 1] + cost  # Substitution or Match
            )

    return dp[len_s1][len_s2]
