# src/solution.py

from collections import Counter

def freq_dist(data):
    if not data:
        raise ValueError("Data cannot be empty.")
    
    total_count = len(data)
    frequency_counter = Counter(data)
    
    relative_frequencies = {
        key: round(count / total_count, 4)
        for key, count in frequency_counter.items()
    }
    
    return relative_frequencies
