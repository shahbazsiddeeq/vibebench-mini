def top_k_words(text, k):
    """
    Returns the top k most frequent words from the text.
    
    Args:
        text: Input text string
        k: Number of top words to return
    
    Returns:
        List of (word, count) tuples, sorted by frequency (descending),
        with ties broken by lexicographic order (ascending)
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(k, int):
        raise TypeError("k must be an integer")
    if k < 0:
        raise ValueError("k must be non-negative")
    
    # Handle empty text
    if not text:
        return []
    
    # Convert to lowercase for case-insensitive processing
    text = text.lower()
    
    # Extract alphanumeric tokens
    words = []
    current_word = []
    
    for char in text:
        if char.isalnum():
            current_word.append(char)
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
        if word:  # Skip empty strings
            word_count[word] = word_count.get(word, 0) + 1
    
    # Sort by frequency (descending) then by word (ascending)
    # Using negative count for descending frequency, then word for ascending lexicographic
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    
    # Return top k
    return sorted_words[:k]
