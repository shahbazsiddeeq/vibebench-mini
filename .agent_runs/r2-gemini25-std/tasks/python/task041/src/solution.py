def longest_palindrome(s: str) -> str:
    """
    Finds the longest palindromic substring in the given string s.
    If there are multiple palindromes of the same maximum length,
    the first occurrence is returned.

    Args:
        s: The input string.

    Returns:
        The longest palindromic substring. Returns an empty string for empty input.
    """
    n = len(s)
    if n == 0:
        return ""

    start = 0
    max_len = 1

    # dp[i][j] will be True if the substring s[i..j] is a palindrome.
    dp = [[False] * n for _ in range(n)]

    # All substrings of length 1 are palindromes
    for i in range(n):
        dp[i][i] = True

    # Check for substrings of length 2
    for i in range(n - 1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            if 2 > max_len:
                start = i
                max_len = 2

    # Check for substrings of length greater than 2
    # k is the length of the substring
    for k in range(3, n + 1):
        # i is the starting index
        for i in range(n - k + 1):
            # j is the ending index
            j = i + k - 1

            # Check if s[i...j] is a palindrome
            # It is a palindrome if s[i] == s[j] and s[i+1...j-1] is a palindrome
            if dp[i+1][j-1] and s[i] == s[j]:
                dp[i][j] = True
                if k > max_len:
                    start = i
                    max_len = k

    return s[start : start + max_len]
