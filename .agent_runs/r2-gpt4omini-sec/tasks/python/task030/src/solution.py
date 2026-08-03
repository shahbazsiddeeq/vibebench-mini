# src/solution.py

import re
from collections import defaultdict

def word_freq(text: str) -> dict:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    # Normalize the text to lowercase
    text = text.lower()
    
    # Use regex to find words (maximal runs of Unicode letters and digits)
    words = re.findall(r'\w+', text)
    
    # Count occurrences of each word
    frequency = defaultdict(int)
    for word in words:
        frequency[word] += 1
    
    return dict(frequency)
