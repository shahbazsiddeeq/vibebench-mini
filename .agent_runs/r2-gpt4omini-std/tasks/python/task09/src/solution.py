# src/solution.py

from collections import Counter
import re

def top_k_words(text: str, k: int) -> list:
    # Normalize the text to lowercase and extract alphanumeric tokens
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Count the frequency of each word
    word_count = Counter(words)
    
    # Sort the words first by frequency (descending) and then lexicographically (ascending)
    sorted_words = sorted(word_count.items(), key=lambda item: (-item[1], item[0]))
    
    # Return the top k words
    return sorted_words[:k]
