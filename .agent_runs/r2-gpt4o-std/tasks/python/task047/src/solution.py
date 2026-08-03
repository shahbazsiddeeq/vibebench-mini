def text_stats(text):
    # Calculate character count
    char_count = len(text)
    
    # Calculate word count
    words = text.split()
    word_count = len(words)
    
    # Calculate sentence count
    import re
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip() != ''])
    
    # Calculate average word length
    if word_count > 0:
        avg_word_length = round(sum(len(word) for word in words) / word_count, 2)
    else:
        avg_word_length = 0.0
    
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length
    }
