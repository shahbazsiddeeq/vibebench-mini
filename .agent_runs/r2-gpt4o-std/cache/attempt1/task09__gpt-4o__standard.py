# src/solution.py

import re
from collections import Counter

def top_k_words(text, k):
    # Use regex to find all alphanumeric words, case-insensitive
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Count the frequency of each word
    word_count = Counter(words)
    
    # Sort by frequency (descending) and then lexicographically (ascending)
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    
    # Return the top k words
    return sorted_words[:k]
