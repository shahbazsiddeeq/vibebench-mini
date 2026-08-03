def is_palindrome(s: str) -> bool:
    """
    Checks if a string is a palindrome after filtering for ASCII alphanumeric
    characters and converting to lowercase.

    Args:
        s: The input string.

    Returns:
        True if the filtered string is a palindrome, False otherwise.
    """
    if not isinstance(s, str):
        # For security and robustness, ensure the input is a string.
        # If not, it cannot be a palindrome in the context of this function.
        # Alternatively, one could raise a TypeError, but returning False
        # is often more graceful for invalid types in such checks.
        return False

    filtered_chars = []
    for char in s:
        # Only keep ASCII alphanumeric characters.
        # This implicitly handles non-ASCII characters by ignoring them.
        if '0' <= char <= '9' or 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            filtered_chars.append(char.lower())

    processed_s = "".join(filtered_chars)

    # An empty string or a string that reduces to empty after filtering is a palindrome.
    # This is handled correctly by the slicing comparison below.
    return processed_s == processed_s[::-1]
