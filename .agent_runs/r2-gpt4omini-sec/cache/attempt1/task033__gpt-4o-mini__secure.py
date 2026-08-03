# src/solution.py

from collections import defaultdict

def group_anagrams(words):
    if not isinstance(words, list) or not all(isinstance(word, str) for word in words):
        raise ValueError("Input must be a list of strings.")
    
    anagrams = defaultdict(list)

    for word in words:
        # Sort the word to find its anagram group
        sorted_word = ''.join(sorted(word))
        anagrams[sorted_word].append(word)

    # Sort each group and the groups themselves
    grouped_anagrams = [sorted(group) for group in anagrams.values()]
    grouped_anagrams.sort(key=lambda x: x[0] if x else "")

    return grouped_anagrams
