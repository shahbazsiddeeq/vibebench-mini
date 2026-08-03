import re
from collections import Counter
from typing import List, Tuple


def top_k_words(text: str, k: int) -> List[Tuple[str, int]]:
    """
    Extract the top-k most frequent words from text.
    
    Args:
        text: Input text to analyze
        k: Number of top words to return
        
    Returns:
        List of (word, count) tuples sorted by:
        1. Frequency (descending)
        2. Lexicographic order (ascending) for ties
    """
    # Validate inputs
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(k, int) or k < 0:
        raise ValueError("k must be a non-negative integer")
    
    # Handle empty text
    if not text:
        return []
    
    # Convert to lowercase and extract alphanumeric tokens
    # Split on non-alphanumeric characters and filter empty strings
    words = re.findall(r'[a-z0-9]+', text.lower())
    
    # Handle case where no valid words found
    if not words:
        return []
    
    # Count word frequencies
    word_counts = Counter(words)
    
    # Sort by:
    # 1. Frequency (descending) - use negative count
    # 2. Lexicographic order (ascending) - use word directly
    sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Return top k results
    return sorted_words[:k]
