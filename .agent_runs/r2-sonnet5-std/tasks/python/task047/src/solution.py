import re


def text_stats(text):
    char_count = len(text)
    words = text.split()
    word_count = len(words)
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = len(sentences)
    if words:
        avg_word_length = round(sum(len(w) for w in words) / word_count, 2)
    else:
        avg_word_length = 0.0
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
