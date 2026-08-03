# src/solution.py

from collections import defaultdict

def group_anagrams(words):
    anagrams = defaultdict(list)
    
    for word in words:
        # Sort the word to get the key
        key = ''.join(sorted(word))
        anagrams[key].append(word)
    
    # Sort each group and then sort the groups by the first element
    result = [sorted(group) for group in anagrams.values()]
    result.sort(key=lambda x: x[0])
    
    return result
