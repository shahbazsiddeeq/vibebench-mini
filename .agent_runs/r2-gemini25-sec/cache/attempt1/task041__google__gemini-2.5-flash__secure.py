def longest_palindrome(s: str) -> str:
    """
    Finds the longest palindromic substring in a given string.

    Args:
        s: The input string.

    Returns:
        The longest palindromic substring. If there are multiple palindromes
        of the same maximum length, the first occurrence is returned.
        Returns an empty string if the input is empty or not a string.
    """
    if not isinstance(s, str):
        # For security and robustness, handle non-string inputs gracefully.
        # Although the problem implies string input, explicit validation is good practice.
        return ""

    n = len(s)
    if n == 0:
        return ""

    # dp[i][j] will be True if the substring s[i..j] is a palindrome.
    # Initialize with False.
    dp = [[False] * n for _ in range(n)]

    longest_pal = ""
    max_length = 0

    # All single characters are palindromes
    for i in range(n):
        dp[i][i] = True
        if max_length == 0:  # Initialize with the first single character
            longest_pal = s[i]
            max_length = 1

    # Check for palindromes of length 2
    for i in range(n - 1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            if 2 > max_length:
                longest_pal = s[i:i+2]
                max_length = 2

    # Check for palindromes of length > 2
    # k is the length of the substring
    for k in range(3, n + 1):
        # i is the starting index
        for i in range(n - k + 1):
            j = i + k - 1  # j is the ending index

            # s[i..j] is a palindrome if s[i] == s[j] and s[i+1..j-1] is a palindrome
            if s[i] == s[j] and dp[i+1][j-1]:
                dp[i][j] = True
                if k > max_length:
                    longest_pal = s[i:j+1]
                    max_length = k

    return longest_pal
