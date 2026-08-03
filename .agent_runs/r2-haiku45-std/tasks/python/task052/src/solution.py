def find_anagram_pairs(words):
    """
    Find unique anagram pairs from a list of words.
    
    Returns a list of unique (a, b) tuples where a and b are two DISTINCT words
    from the input that are anagrams of each other, with a < b lexicographically.
    Comparison is case-sensitive. Identical words are never paired with themselves.
    The returned list is sorted in ascending order.
    """
    # Group words by their sorted characters (anagram signature)
    anagram_groups = {}
    
    for word in words:
        # Create a signature by sorting the characters
        signature = ''.join(sorted(word))
        if signature not in anagram_groups:
            anagram_groups[signature] = []
        anagram_groups[signature].append(word)
    
    # Find pairs within each anagram group
    pairs = []
    
    for signature, group in anagram_groups.items():
        # Remove duplicates while preserving the ability to find pairs
        unique_words = list(set(group))
        
        # Only process groups with at least 2 distinct words
        if len(unique_words) >= 2:
            # Generate all pairs from distinct words
            for i in range(len(unique_words)):
                for j in range(i + 1, len(unique_words)):
                    word_a = unique_words[i]
                    word_b = unique_words[j]
                    
                    # Ensure lexicographic order (a < b)
                    if word_a < word_b:
                        pairs.append((word_a, word_b))
                    else:
                        pairs.append((word_b, word_a))
    
    # Sort the pairs and return
    pairs.sort()
    return pairs
