# src/solution.py

from typing import List, Tuple
from collections import defaultdict

def find_anagram_pairs(words: List[str]) -> List[Tuple[str, str]]:
    # Validate input
    if not isinstance(words, list) or not all(isinstance(word, str) for word in words):
        raise ValueError("Input must be a list of strings.")
    
    # Dictionary to hold sorted word as key and original words as values
    anagram_map = defaultdict(set)

    # Populate the anagram map
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_map[sorted_word].add(word)

    # Find unique anagram pairs
    anagram_pairs = set()
    for word_set in anagram_map.values():
        word_list = sorted(word_set)  # Sort to ensure lexicographic order
        for i in range(len(word_list)):
            for j in range(i + 1, len(word_list)):
                anagram_pairs.add((word_list[i], word_list[j]))

    # Return sorted list of unique pairs
    return sorted(anagram_pairs)
