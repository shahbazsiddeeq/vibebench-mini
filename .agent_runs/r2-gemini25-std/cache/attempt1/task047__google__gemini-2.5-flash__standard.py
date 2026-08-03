import re


def text_stats(text):
    char_count = len(text)
    words = text.split()
    word_count = len(words)

    # Calculate sentence count
    # Split by one or more occurrences of '.', '!', '?'
    sentences = re.split(r"[.!?]+", text)
    # Filter out empty strings that result from splitting (e.g., "Hello!!")
    sentence_count = len([s for s in sentences if s.strip()])

    # Calculate average word length
    if word_count > 0:
        total_word_length = sum(len(word) for word in words)
        avg_word_length = round(total_word_length / word_count, 2)
    else:
        avg_word_length = 0.0

    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_length": avg_word_length,
    }
