def word_freq(text):
    """
    Count word frequencies in text.
    
    A word is a maximal run of Unicode letters and digits.
    Every other character (whitespace, punctuation, apostrophes, hyphens, underscores)
    is a separator and is not part of a word.
    Words are lowercased before counting.
    
    Args:
        text: Input string to analyze
        
    Returns:
        Dictionary mapping lowercase words to their frequencies
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    if not text:
        return {}
    
    # Convert to lowercase
    text = text.lower()
    
    # Extract words: maximal runs of letters and digits
    words = []
    current_word = []
    
    for char in text:
        # Check if character is a letter or digit (Unicode-aware)
        if char.isalnum():
            current_word.append(char)
        else:
            # Character is a separator
            if current_word:
                words.append(''.join(current_word))
                current_word = []
    
    # Don't forget the last word if text doesn't end with a separator
    if current_word:
        words.append(''.join(current_word))
    
    # Count frequencies
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    
    return freq
