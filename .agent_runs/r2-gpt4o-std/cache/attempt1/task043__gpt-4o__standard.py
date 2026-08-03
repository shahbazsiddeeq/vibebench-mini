# src/solution.py

def edit_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    
    # Create a matrix to store distances
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]
    
    # Initialize the matrix
    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j
    
    # Compute the edit distance
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,    # Deletion
                    dp[i][j - 1] + 1,    # Insertion
                    dp[i - 1][j - 1] + 1 # Replacement
                )
    
    return dp[len_s1][len_s2]
