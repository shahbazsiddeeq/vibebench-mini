# src/solution.py

from collections import defaultdict
from typing import List, Tuple

def find_anagram_pairs(words: List[str]) -> List[Tuple[str, str]]:
    def is_valid_word(word: str) -> bool:
        return isinstance(word, str) and word.isalpha()

    # Validate input
    if not isinstance(words, list) or not all(is_valid_word(word) for word in words):
        raise ValueError("Input must be a list of alphabetic strings.")

    # Dictionary to store sorted word as key and list of original words as values
    anagram_dict = defaultdict(list)

    # Populate the dictionary
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_dict[sorted_word].append(word)

    # Find all unique anagram pairs
    anagram_pairs = set()
    for word_list in anagram_dict.values():
        if len(word_list) > 1:
            # Sort the list to ensure lexicographic order
            word_list = sorted(set(word_list))
            for i in range(len(word_list)):
                for j in range(i + 1, len(word_list)):
                    anagram_pairs.add((word_list[i], word_list[j]))

    # Return sorted list of anagram pairs
    return sorted(anagram_pairs)
