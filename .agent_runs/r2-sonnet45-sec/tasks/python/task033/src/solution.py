def group_anagrams(words):
    """
    Groups words that are anagrams of each other.
    
    Args:
        words: A list of strings to group by anagrams
        
    Returns:
        A list of lists, where each inner list contains anagrams grouped together.
        Each group is sorted alphabetically, and groups are sorted by their first element.
    """
    # Input validation
    if not isinstance(words, list):
        raise TypeError("Input must be a list")
    
    # Handle empty list
    if not words:
        return []
    
    # Validate all elements are strings
    for word in words:
        if not isinstance(word, str):
            raise TypeError("All elements must be strings")
    
    # Dictionary to group anagrams
    # Key: sorted tuple of characters (canonical form)
    # Value: list of words that are anagrams
    anagram_groups = {}
    
    for word in words:
        # Create a canonical form by sorting the characters
        # Using tuple of sorted characters as the key
        sorted_chars = tuple(sorted(word))
        
        if sorted_chars not in anagram_groups:
            anagram_groups[sorted_chars] = []
        
        anagram_groups[sorted_chars].append(word)
    
    # Sort each group alphabetically
    result = []
    for group in anagram_groups.values():
        sorted_group = sorted(group)
        result.append(sorted_group)
    
    # Sort groups by their first element
    result.sort(key=lambda group: group[0])
    
    return result
