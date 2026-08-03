def is_palindrome(s: str) -> bool:
    """
    Checks if a string is a palindrome after filtering for alphanumeric ASCII characters
    and converting to lowercase.

    Args:
        s: The input string.

    Returns:
        True if the filtered string is a palindrome, False otherwise.
    """
    filtered_chars = []
    for char in s:
        if '0' <= char <= '9' or 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            filtered_chars.append(char.lower())

    filtered_s = "".join(filtered_chars)
    return filtered_s == filtered_s[::-1]
