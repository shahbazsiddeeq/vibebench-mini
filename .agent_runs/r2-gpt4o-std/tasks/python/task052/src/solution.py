def find_anagram_pairs(words):
    from collections import defaultdict

    # Dictionary to store sorted word as key and list of original words as values
    anagram_dict = defaultdict(list)

    # Populate the dictionary
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_dict[sorted_word].append(word)

    # Set to store unique anagram pairs
    anagram_pairs = set()

    # Find all unique pairs
    for anagram_list in anagram_dict.values():
        if len(anagram_list) > 1:
            # Sort the list to ensure lexicographic order
            anagram_list.sort()
            for i in range(len(anagram_list)):
                for j in range(i + 1, len(anagram_list)):
                    anagram_pairs.add((anagram_list[i], anagram_list[j]))

    # Convert set to sorted list
    return sorted(anagram_pairs)
