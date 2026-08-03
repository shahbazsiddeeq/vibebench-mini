def group_anagrams(words):
    """
    Groups words that are anagrams together.
    Each group is sorted alphabetically.
    Groups are sorted by their first element.
    
    Args:
        words: List of strings
        
    Returns:
        List of lists, where each inner list contains anagrams
    """
    if not words:
        return []
    
    # Dictionary to group anagrams
    # Key: sorted tuple of characters
    # Value: list of words that are anagrams
    anagram_groups = {}
    
    for word in words:
        # Create a key by sorting the characters in the word
        key = tuple(sorted(word))
        
        if key not in anagram_groups:
            anagram_groups[key] = []
        
        anagram_groups[key].append(word)
    
    # Sort each group alphabetically
    result = []
    for group in anagram_groups.values():
        sorted_group = sorted(group)
        result.append(sorted_group)
    
    # Sort groups by their first element
    result.sort(key=lambda group: group[0])
    
    return result
