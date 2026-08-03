import re
from typing import Dict, Union


def text_stats(text: str) -> Dict[str, Union[int, float]]:
    """
    Calculate text statistics including character count, word count, 
    sentence count, and average word length.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with keys: char_count, word_count, sentence_count, avg_word_length
    """
    # Validate input
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Character count
    char_count = len(text)
    
    # Word count and average word length
    words = text.split()
    word_count = len(words)
    
    if word_count > 0:
        total_word_length = sum(len(word) for word in words)
        avg_word_length = round(total_word_length / word_count, 2)
    else:
        avg_word_length = 0.0
    
    # Sentence count - split on runs of . ! ?
    # Split on one or more occurrences of . ! or ?
    sentences = re.split(r'[.!?]+', text)
    # Filter out empty segments
    sentence_count = len([s for s in sentences if s.strip()])
    
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
