import re

def text_stats(text):
    """
    Calculate text statistics including character count, word count, 
    sentence count, and average word length.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        dict: A dictionary with keys:
            - char_count (int): total number of characters
            - word_count (int): number of whitespace-separated tokens
            - sentence_count (int): number of sentences (split on . ! ?)
            - avg_word_length (float): mean length of words, rounded to 2 decimal places
    """
    char_count = len(text)
    
    words = text.split()
    word_count = len(words)
    
    # Calculate average word length
    if word_count > 0:
        total_word_length = sum(len(word) for word in words)
        avg_word_length = round(total_word_length / word_count, 2)
    else:
        avg_word_length = 0.0
    
    # Count sentences by splitting on . ! ?
    # Split on runs of these characters and filter out empty segments
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
