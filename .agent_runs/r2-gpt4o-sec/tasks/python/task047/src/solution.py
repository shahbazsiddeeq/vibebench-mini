def text_stats(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    char_count = len(text)
    
    words = text.split()
    word_count = len(words)
    
    sentences = [s for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    sentence_count = len(sentences)
    
    if word_count > 0:
        avg_word_length = round(sum(len(word) for word in words) / word_count, 2)
    else:
        avg_word_length = 0.0

    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
