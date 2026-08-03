def find_anagram_pairs(words):
    """
    Finds unique (a, b) tuples where a and b are two distinct words from the input
    that are anagrams of each other, with a < b lexicographically.

    Comparison is case-sensitive. Identical words are never paired with themselves.
    The returned list is sorted in ascending order.

    Args:
        words: A list of strings.

    Returns:
        A list of unique (str, str) tuples representing anagram pairs.
    """
    anagram_map = {}
    for word in words:
        # Create a canonical representation for each word (sorted characters)
        # This representation will be the same for all anagrams
        canonical_form = "".join(sorted(word))
        if canonical_form not in anagram_map:
            anagram_map[canonical_form] = set()
        anagram_map[canonical_form].add(word)

    result_pairs = set()
    for canonical_form in anagram_map:
        current_anagrams = sorted(list(anagram_map[canonical_form]))
        # Iterate through all unique words that are anagrams of each other
        for i in range(len(current_anagrams)):
            for j in range(i + 1, len(current_anagrams)):
                word1 = current_anagrams[i]
                word2 = current_anagrams[j]
                # Ensure distinct words and lexicographical order
                if word1 != word2:
                    if word1 < word2:
                        result_pairs.add((word1, word2))
                    else:
                        result_pairs.add((word2, word1))

    # Sort the final list of pairs
    return sorted(list(result_pairs))
