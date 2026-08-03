import re
from collections import Counter

def top_k_words(text, k):
    """
    Returns the top k most frequent words from the text.
    
    Args:
        text: Input text string
        k: Number of top words to return
        
    Returns:
        List of (word, count) tuples sorted by:
        1. Frequency (descending)
        2. Lexicographic order (ascending) for ties
    """
    if not text:
        return []
    
    # Convert to lowercase and extract alphanumeric tokens
    words = re.findall(r'\b\w+\b', text.lower())
    
    if not words:
        return []
    
    # Count word frequencies
    word_counts = Counter(words)
    
    # Sort by count (descending), then by word (ascending) for ties
    sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Return top k
    return sorted_words[:k]
