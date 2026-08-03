# src/solution.py

def text_stats(text: str) -> dict:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
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
    avg_word_length = 0.0
    if word_count > 0:
        total_word_length = sum(len(word) for word in words)
        avg_word_length = round(total_word_length / word_count, 2)
    
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
