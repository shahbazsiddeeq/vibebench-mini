def group_anagrams(words):
    """
    Groups words that are anagrams of each other.
    Each group is sorted alphabetically.
    Groups are sorted by their first element.
    
    Args:
        words: List of strings
        
    Returns:
        List of lists, where each inner list contains anagrams sorted alphabetically,
        and the outer list is sorted by the first element of each group.
    """
    if not words:
        return []
    
    # Dictionary to group anagrams
    # Key: sorted characters of the word (canonical form)
    # Value: list of words that are anagrams
    anagram_groups = {}
    
    for word in words:
        # Sort the characters to get the canonical form
        sorted_word = ''.join(sorted(word))
        
        if sorted_word not in anagram_groups:
            anagram_groups[sorted_word] = []
        
        anagram_groups[sorted_word].append(word)
    
    # Sort each group alphabetically and convert to list of lists
    result = []
    for group in anagram_groups.values():
        result.append(sorted(group))
    
    # Sort groups by their first element
    result.sort(key=lambda group: group[0])
    
    return result
