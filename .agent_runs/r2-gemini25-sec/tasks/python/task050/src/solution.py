def unique_char_count(s: str) -> dict[str, int]:
    """
    Counts characters that appear exactly once in a string,
    preserving their first appearance order.

    Args:
        s: The input string.

    Returns:
        A dictionary where keys are characters that appear exactly once,
        values are 1, and keys are ordered by their first appearance in s.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    if not s:
        return {}

    char_counts = {}
    # Use a separate ordered dictionary to track first appearance and count
    # This allows us to iterate through the string once to get counts
    # and then iterate through this ordered dict to build the final result
    # in the correct order.
    ordered_char_tracker = {}

    for char in s:
        # For security and robustness, ensure character is a single character string
        # Although Python's iteration handles this, explicit check adds clarity
        if not isinstance(char, str) or len(char) != 1:
            # This case should ideally not happen with a valid string input,
            # but defensive programming suggests handling unexpected data.
            continue 

        ordered_char_tracker[char] = ordered_char_tracker.get(char, 0) + 1

    result = {}
    for char, count in ordered_char_tracker.items():
        if count == 1:
            result[char] = 1

    return result
