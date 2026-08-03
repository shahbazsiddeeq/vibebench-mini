def group_anagrams(words):
    """
    Groups words that are anagrams.

    Each group is sorted alphabetically.
    Groups are sorted by their first element.

    Args:
        words: A list of strings.

    Returns:
        A list of lists of strings, where each inner list contains anagrams.
    """
    if not words:
        return []

    anagram_map = {}
    for word in words:
        # Create a canonical representation for each word (sorted tuple of characters)
        # This allows us to use it as a dictionary key.
        canonical_form = tuple(sorted(word))
        if canonical_form not in anagram_map:
            anagram_map[canonical_form] = []
        anagram_map[canonical_form].append(word)

    # Prepare the result list
    result = []
    for canonical_form in anagram_map:
        # Sort each group alphabetically
        anagram_map[canonical_form].sort()
        result.append(anagram_map[canonical_form])

    # Sort the groups by their first element
    result.sort(key=lambda group: group[0])

    return result
