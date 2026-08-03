def is_palindrome(s: str) -> bool:
    filtered = [c.lower() for c in s if c.isascii() and c.isalnum()]
    return filtered == filtered[::-1]
