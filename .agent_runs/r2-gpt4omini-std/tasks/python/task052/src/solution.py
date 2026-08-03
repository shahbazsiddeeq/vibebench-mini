# src/solution.py

def find_anagram_pairs(words):
    from collections import defaultdict

    anagrams = defaultdict(list)

    # Group words by their sorted character tuple
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagrams[sorted_word].append(word)

    result = set()

    # Create pairs from the grouped anagrams
    for group in anagrams.values():
        if len(group) > 1:
            group = sorted(set(group))  # Remove duplicates and sort
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    result.add((group[i], group[j]))

    return sorted(result)
