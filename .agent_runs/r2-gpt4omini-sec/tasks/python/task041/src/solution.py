# src/solution.py

def longest_palindrome(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    s = s.strip()  # Sanitize input by stripping whitespace
    n = len(s)
    
    if n == 0:
        return ""
    
    start, end = 0, 0

    def expand_around_center(left: int, right: int) -> int:
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    for i in range(n):
        len1 = expand_around_center(i, i)      # Odd length palindromes
        len2 = expand_around_center(i, i + 1)  # Even length palindromes
        max_len = max(len1, len2)
        
        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2

    return s[start:end + 1]
