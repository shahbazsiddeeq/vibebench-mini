import re


def is_palindrome(s: str) -> bool:
    norm = re.sub(r"[^A-Za-z0-9]", "", s).lower()
    return norm == norm[::-1]
