def longest_palindrome(s: str) -> str:
    """
    Returns the longest palindromic substring in the given string.
    If there are multiple palindromes of the same length, returns the first occurrence.
    Returns empty string for empty input.
    
    Args:
        s: Input string to search for palindromic substrings
        
    Returns:
        The longest palindromic substring, or empty string if input is empty
    """
    # Input validation
    if not isinstance(s, str):
        return ""
    
    # Handle empty string
    if len(s) == 0:
        return ""
    
    # Handle single character
    if len(s) == 1:
        return s
    
    # Helper function to expand around center and find palindrome length
    def expand_around_center(left: int, right: int) -> tuple:
        """
        Expands around a center point to find the longest palindrome.
        Returns (start_index, length) of the palindrome.
        """
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # left and right are now one step beyond the palindrome
        length = right - left - 1
        start = left + 1
        return (start, length)
    
    max_start = 0
    max_length = 1
    
    # Check all possible centers (both odd and even length palindromes)
    for i in range(len(s)):
        # Odd length palindromes (single character center)
        start, length = expand_around_center(i, i)
        if length > max_length:
            max_length = length
            max_start = start
        
        # Even length palindromes (between two characters)
        if i < len(s) - 1:
            start, length = expand_around_center(i, i + 1)
            if length > max_length:
                max_length = length
                max_start = start
    
    return s[max_start:max_start + max_length]
