def reverse_words(s: str) -> str:
    """
    Reverses the order of words in a string.

    Words are maximal runs of non-whitespace characters. Any run of whitespace
    (spaces, tabs, newlines) acts as a separator and is collapsed.
    Leading/trailing whitespace is ignored.
    An empty string or a string containing only whitespace returns "".

    Args:
        s: The input string.

    Returns:
        A string with the whitespace-separated words of s in reverse order,
        joined by a single space.
    """
    if not s or s.isspace():
        return ""

    # Split the string by any whitespace, which handles multiple spaces
    # and different types of whitespace characters.
    # The split() method without arguments handles leading/trailing whitespace
    # and multiple internal spaces correctly by returning an empty list
    # or filtering out empty strings from the result.
    words = s.split()

    # Reverse the list of words
    words.reverse()

    # Join the reversed words with a single space
    return " ".join(words)
