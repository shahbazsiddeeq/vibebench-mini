def longest_palindrome(s: str) -> str:
    """Return the longest palindromic substring, preferring the first on ties."""
    if not s:
        return ""

    best_start = 0
    best_length = 1

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        start = left + 1
        return start, right - start

    for center in range(len(s)):
        for left, right in ((center, center), (center, center + 1)):
            start, length = expand(left, right)
            if length > best_length or (
                length == best_length and start < best_start
            ):
                best_start = start
                best_length = length

    return s[best_start : best_start + best_length]
