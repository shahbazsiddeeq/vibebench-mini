def find_anagram_pairs(words):
    """
    Find all unique pairs of distinct words that are anagrams of each other.
    
    Args:
        words: List of strings
        
    Returns:
        List of tuples (a, b) where a and b are anagrams and a < b lexicographically
    """
    from collections import defaultdict
    
    # Group words by their sorted character signature
    anagram_groups = defaultdict(set)
    
    for word in words:
        # Use sorted characters as the key
        signature = ''.join(sorted(word))
        anagram_groups[signature].add(word)
    
    # Generate pairs from each group
    pairs = set()
    
    for group in anagram_groups.values():
        # Only process groups with at least 2 distinct words
        if len(group) >= 2:
            # Convert to sorted list for consistent ordering
            word_list = sorted(group)
            # Generate all pairs
            for i in range(len(word_list)):
                for j in range(i + 1, len(word_list)):
                    pairs.add((word_list[i], word_list[j]))
    
    # Return sorted list of pairs
    return sorted(pairs)
