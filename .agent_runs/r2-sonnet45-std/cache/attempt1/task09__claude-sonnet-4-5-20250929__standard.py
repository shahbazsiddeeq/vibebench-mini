def top_k_words(text, k):
    """
    Returns the top k most frequent words from the text.
    
    Args:
        text: Input string
        k: Number of top words to return
    
    Returns:
        List of tuples (word, count) sorted by:
        1. Count (descending)
        2. Word lexicographically (ascending) for ties
    """
    if not text:
        return []
    
    # Extract alphanumeric tokens, convert to lowercase
    words = []
    current_word = []
    
    for char in text:
        if char.isalnum():
            current_word.append(char.lower())
        else:
            if current_word:
                words.append(''.join(current_word))
                current_word = []
    
    # Don't forget the last word if text doesn't end with separator
    if current_word:
        words.append(''.join(current_word))
    
    # Count word frequencies
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    # Sort by count (descending), then by word (ascending)
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    
    # Return top k
    return sorted_words[:k]
