import collections

def group_anagrams(words):
    """
    Groups words that are anagrams. Each group is sorted alphabetically,
    and the groups themselves are sorted by their first element.

    Args:
        words: A list of strings. Each string should consist of lowercase
               English letters.

    Returns:
        A list of lists of strings, where each inner list contains anagrams.
        Returns an empty list if the input is invalid or empty.
    """
    if not isinstance(words, list):
        return []

    # Use a defaultdict to store anagrams. The key will be a sorted tuple of characters
    # (canonical form of an anagram), and the value will be a list of words.
    anagram_map = collections.defaultdict(list)

    for word in words:
        if not isinstance(word, str):
            # Skip or handle non-string elements gracefully
            continue
        if not word.islower() and word.isalpha():
            # If it contains non-lowercase letters but is alphabetic,
            # we could normalize it, but for strict security/input validation,
            # we'll treat it as invalid if not strictly lowercase.
            # For this problem, assuming lowercase English letters as per typical constraints.
            continue
        if not word.isalpha() and word != "":
            # If it contains non-alphabetic characters (e.g., numbers, symbols)
            # and is not an empty string, it's invalid for anagram grouping.
            continue

        # Create a canonical representation of the word by sorting its characters.
        # This sorted string/tuple will be the key for our anagram map.
        # Using a tuple for the key makes it immutable and hashable.
        canonical_form = tuple(sorted(word))
        anagram_map[canonical_form].append(word)

    # Prepare the result list.
    result = []
    for key in anagram_map:
        # Sort each group alphabetically as required.
        current_group = sorted(anagram_map[key])
        result.append(current_group)

    # Sort the groups by their first element.
    # The lambda function ensures stable sorting based on the first element of each inner list.
    result.sort(key=lambda x: x[0])

    return result
