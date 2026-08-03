# src/solution.py

def text_stats(text: str) -> dict:
    # Calculate character count
    char_count = len(text)
    
    # Calculate word count
    words = text.split()
    word_count = len(words)
    
    # Calculate sentence count
    sentences = [s for s in text.split('.') if s.strip()] + \
                [s for s in text.split('!') if s.strip()] + \
                [s for s in text.split('?') if s.strip()]
    sentence_count = len(sentences)
    
    # Calculate average word length
    avg_word_length = (sum(len(word) for word in words) / word_count) if word_count > 0 else 0.0
    avg_word_length = round(avg_word_length, 2)
    
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
