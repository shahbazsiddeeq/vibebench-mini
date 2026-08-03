# src/solution.py

from collections import defaultdict

def group_anagrams(words):
    anagrams = defaultdict(list)
    
    for word in words:
        # Sort the word to find its anagram group
        sorted_word = ''.join(sorted(word))
        anagrams[sorted_word].append(word)
    
    # Sort each group and the groups themselves
    grouped_anagrams = [sorted(group) for group in anagrams.values()]
    return sorted(grouped_anagrams, key=lambda x: x[0] if x else "")
