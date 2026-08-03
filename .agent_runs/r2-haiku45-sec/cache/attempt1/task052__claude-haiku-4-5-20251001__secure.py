def find_anagram_pairs(words):
    """
    Find unique pairs of distinct anagrams from a list of words.
    
    Args:
        words: A list of strings to check for anagrams
        
    Returns:
        A sorted list of tuples (a, b) where a and b are anagrams with a < b lexicographically
    """
    # Input validation
    if not isinstance(words, list):
        return []
    
    # Filter out non-string elements and validate
    validated_words = []
    for word in words:
        if isinstance(word, str):
            validated_words.append(word)
    
    if len(validated_words) < 2:
        return []
    
    # Group words by their sorted characters (anagram signature)
    # This creates a mapping from sorted characters to list of words
    anagram_groups = {}
    
    for word in validated_words:
        # Create a signature by sorting the characters in the word
        signature = ''.join(sorted(word))
        
        if signature not in anagram_groups:
            anagram_groups[signature] = []
        
        anagram_groups[signature].append(word)
    
    # Find pairs within each anagram group
    pairs = []
    
    for signature, group in anagram_groups.items():
        # Only process groups with at least 2 words
        if len(group) < 2:
            continue
        
        # Get unique words in this group (remove duplicates)
        unique_words = list(set(group))
        
        # Only process if we still have at least 2 distinct words
        if len(unique_words) < 2:
            continue
        
        # Sort the unique words lexicographically
        unique_words.sort()
        
        # Generate all pairs (a, b) where a < b
        for i in range(len(unique_words)):
            for j in range(i + 1, len(unique_words)):
                pairs.append((unique_words[i], unique_words[j]))
    
    # Sort the pairs list
    pairs.sort()
    
    return pairs
