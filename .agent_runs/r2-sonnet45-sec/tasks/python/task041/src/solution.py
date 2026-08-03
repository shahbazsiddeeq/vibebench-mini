def longest_palindrome(s: str) -> str:
    """
    Returns the longest palindromic substring in s.
    Returns the first occurrence if there are multiple palindromes of the same length.
    Returns empty string for empty input.
    
    Args:
        s: Input string to search for palindromes
        
    Returns:
        The longest palindromic substring
    """
    # Input validation
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # Handle empty string
    if not s:
        return ""
    
    # Handle single character
    if len(s) == 1:
        return s
    
    def expand_around_center(left: int, right: int) -> str:
        """
        Expand around center to find palindrome.
        
        Args:
            left: Left index of center
            right: Right index of center
            
        Returns:
            Palindromic substring found by expanding from center
        """
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the valid palindrome (left and right are one step beyond)
        return s[left + 1:right]
    
    longest = ""
    
    # Check each possible center
    for i in range(len(s)):
        # Odd length palindromes (single character center)
        palindrome1 = expand_around_center(i, i)
        if len(palindrome1) > len(longest):
            longest = palindrome1
        
        # Even length palindromes (two character center)
        if i + 1 < len(s):
            palindrome2 = expand_around_center(i, i + 1)
            if len(palindrome2) > len(longest):
                longest = palindrome2
    
    return longest
