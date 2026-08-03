def unique_char_count(s: str) -> dict[str, int]:
    """
    Returns a dict mapping each character that appears exactly once in s to 1,
    with keys ordered by first appearance in s.

    Args:
        s: The input string.

    Returns:
        A dictionary where keys are characters that appear exactly once in s,
        values are 1, and keys are ordered by their first appearance in s.
    """
    char_counts = {}
    # First pass to count character frequencies
    for char in s:
        char_counts[char] = char_counts.get(char, 0) + 1

    # Second pass to build the result dictionary, preserving insertion order
    # for characters that appear exactly once.
    result = {}
    for char in s:
        if char_counts[char] == 1:
            # Add to result only if it's not already there
            # This ensures first appearance order for keys
            if char not in result:
                result[char] = 1
    return result
