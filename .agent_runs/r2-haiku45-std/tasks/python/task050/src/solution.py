def unique_char_count(s):
    """
    Returns a dict mapping each character that appears exactly once in s to 1,
    with keys ordered by first appearance in s.
    
    Args:
        s: A string
        
    Returns:
        A dict with characters that appear exactly once, mapped to 1,
        ordered by first appearance
    """
    # Count occurrences of each character
    char_counts = {}
    for char in s:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    # Build result dict with characters that appear exactly once,
    # preserving first appearance order
    result = {}
    for char in s:
        if char_counts[char] == 1 and char not in result:
            result[char] = 1
    
    return result
