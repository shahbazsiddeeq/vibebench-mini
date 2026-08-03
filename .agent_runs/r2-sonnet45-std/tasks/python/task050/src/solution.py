def unique_char_count(s):
    """
    Returns a dict mapping each character that appears exactly once in s to 1,
    with keys ordered by first appearance in s.
    
    Args:
        s: Input string
        
    Returns:
        Dict with characters appearing exactly once, mapped to 1
    """
    # Count occurrences of each character
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    # Build result dict with only characters that appear exactly once
    # Iterate through s to preserve first-appearance order
    result = {}
    for char in s:
        if char_count[char] == 1 and char not in result:
            result[char] = 1
    
    return result
