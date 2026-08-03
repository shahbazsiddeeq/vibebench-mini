# src/solution.py

def longest_palindrome(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    n = len(s)
    if n == 0:
        return ""
    
    start, max_length = 0, 1
    
    def expand_around_center(left: int, right: int) -> None:
        nonlocal start, max_length
        while left >= 0 and right < n and s[left] == s[right]:
            current_length = right - left + 1
            if current_length > max_length:
                start = left
                max_length = current_length
            left -= 1
            right += 1
    
    for i in range(n):
        expand_around_center(i, i)       # Odd length palindromes
        expand_around_center(i, i + 1)   # Even length palindromes
    
    return s[start:start + max_length]
