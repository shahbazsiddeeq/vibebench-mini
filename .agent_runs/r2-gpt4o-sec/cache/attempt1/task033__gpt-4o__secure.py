# src/solution.py

from collections import defaultdict

def group_anagrams(words):
    if not isinstance(words, list):
        raise ValueError("Input must be a list of strings.")
    
    anagrams = defaultdict(list)
    
    for word in words:
        if not isinstance(word, str):
            raise ValueError("All elements in the list must be strings.")
        sorted_word = ''.join(sorted(word))
        anagrams[sorted_word].append(word)
    
    result = []
    for group in anagrams.values():
        result.append(sorted(group))
    
    return sorted(result, key=lambda x: x[0])
