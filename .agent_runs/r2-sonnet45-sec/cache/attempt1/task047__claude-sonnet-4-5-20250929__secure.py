import re


def text_stats(text):
    """
    Calculate statistics for the given text.
    
    Args:
        text: A string to analyze
        
    Returns:
        A dictionary with char_count, word_count, sentence_count, and avg_word_length
    """
    # Validate input
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Character count: total length including spaces and punctuation
    char_count = len(text)
    
    # Word count: whitespace-separated tokens
    words = text.split()
    word_count = len(words)
    
    # Sentence count: split on runs of . ! ?
    # Split by one or more sentence-ending punctuation marks
    sentences = re.split(r'[.!?]+', text)
    # Count only non-empty segments
    sentence_count = sum(1 for s in sentences if s.strip())
    
    # Average word length
    if word_count == 0:
        avg_word_length = 0.0
    else:
        total_length = sum(len(word) for word in words)
        avg_word_length = round(total_length / word_count, 2)
    
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
