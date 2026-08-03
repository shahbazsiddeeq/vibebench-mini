def longest_palindrome(s: str) -> str:
    """
    Returns the longest palindromic substring in s.
    If there are multiple palindromes of the same length, returns the first occurrence.
    Returns empty string for empty input.
    """
    if not s:
        return ""
    
    if len(s) == 1:
        return s
    
    def expand_around_center(left: int, right: int) -> tuple[int, int]:
        """Expand around center and return (start, end) of palindrome."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the valid palindrome boundaries
        return left + 1, right - 1
    
    start = 0
    end = 0
    max_length = 0
    
    # Check all possible centers (both odd and even length palindromes)
    for i in range(len(s)):
        # Odd length palindromes (single character center)
        left, right = expand_around_center(i, i)
        length = right - left + 1
        if length > max_length:
            max_length = length
            start = left
            end = right
        
        # Even length palindromes (two character center)
        if i + 1 < len(s):
            left, right = expand_around_center(i, i + 1)
            length = right - left + 1
            if length > max_length:
                max_length = length
                start = left
                end = right
    
    return s[start:end + 1]
