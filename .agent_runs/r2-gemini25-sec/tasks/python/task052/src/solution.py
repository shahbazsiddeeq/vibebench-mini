def find_anagram_pairs(words):
    """
    Finds unique (a, b) tuples where a and b are distinct words from the input
    that are anagrams of each other, with a < b lexicographically.

    Args:
        words: A list of strings.

    Returns:
        A list of unique (a, b) tuples, sorted in ascending order.
    """
    if not isinstance(words, list):
        raise TypeError("Input 'words' must be a list.")

    # Use a dictionary to group words by their sorted character representation (canonical form)
    # This allows efficient lookup of potential anagrams.
    anagram_groups = {}
    for word in words:
        if not isinstance(word, str):
            raise TypeError("All elements in 'words' must be strings.")
        
        # Sanitize input: remove leading/trailing whitespace, though problem implies clean words
        # For this problem, case-sensitivity means we don't lower-case.
        # We also don't remove non-alphanumeric characters as they are part of the word.
        
        # Create a canonical representation for anagram checking
        # Sorting characters makes "eat" and "tea" both become "aet"
        canonical_form = "".join(sorted(word))

        if canonical_form not in anagram_groups:
            anagram_groups[canonical_form] = set()
        anagram_groups[canonical_form].add(word)

    found_pairs = set()
    for canonical_form, group in anagram_groups.items():
        # If a group has more than one word, it contains anagrams
        if len(group) > 1:
            # Convert set to a sorted list to ensure consistent iteration order
            # and to easily pick distinct pairs.
            sorted_group = sorted(list(group))
            
            # Iterate through all unique pairs within the group
            for i in range(len(sorted_group)):
                for j in range(i + 1, len(sorted_group)):
                    word1 = sorted_group[i]
                    word2 = sorted_group[j]
                    
                    # Ensure words are distinct (already handled by j = i + 1)
                    # and lexicographically ordered (already handled by sorted_group and i, j)
                    
                    # Add the pair to the set of found pairs.
                    # The set automatically handles uniqueness of the (a, b) tuple.
                    found_pairs.add((word1, word2))

    # Convert the set of pairs to a list and sort it lexicographically
    # The default tuple sorting works lexicographically.
    return sorted(list(found_pairs))
