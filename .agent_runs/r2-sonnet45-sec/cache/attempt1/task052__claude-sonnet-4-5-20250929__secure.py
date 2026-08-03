def find_anagram_pairs(words):
    """
    Find all unique pairs of distinct words that are anagrams of each other.
    
    Args:
        words: A list of strings
        
    Returns:
        A sorted list of tuples (a, b) where a and b are anagrams and a < b lexicographically
    """
    # Input validation
    if not isinstance(words, list):
        return []
    
    # Validate all elements are strings
    for word in words:
        if not isinstance(word, str):
            return []
    
    # Group words by their sorted character signature
    anagram_groups = {}
    
    for word in words:
        # Create a signature by sorting the characters
        signature = ''.join(sorted(word))
        
        if signature not in anagram_groups:
            anagram_groups[signature] = []
        anagram_groups[signature].append(word)
    
    # Find all pairs within each anagram group
    pairs = set()
    
    for signature, group in anagram_groups.items():
        # Remove duplicates while preserving all instances for pairing
        # We need unique words only
        unique_words = list(set(group))
        
        # Generate all pairs from unique words
        for i in range(len(unique_words)):
            for j in range(i + 1, len(unique_words)):
                word1 = unique_words[i]
                word2 = unique_words[j]
                
                # Ensure lexicographic order (a < b)
                if word1 < word2:
                    pairs.add((word1, word2))
                else:
                    pairs.add((word2, word1))
    
    # Convert to sorted list
    return sorted(list(pairs))
