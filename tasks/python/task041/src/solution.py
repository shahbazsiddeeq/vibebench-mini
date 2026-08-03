from __future__ import annotations


def longest_palindrome(s: str) -> str:
    if not s:
        return ""
    start, end = 0, 0

    def expand(lo: int, r: int) -> tuple[int, int]:
        while lo >= 0 and r < len(s) and s[lo] == s[r]:
            lo -= 1
            r += 1
        return lo + 1, r - 1

    for i in range(len(s)):
        l1, r1 = expand(i, i)
        l2, r2 = expand(i, i + 1)
        if r1 - l1 > end - start:
            start, end = l1, r1
        if r2 - l2 > end - start:
            start, end = l2, r2
    return s[start : end + 1]
