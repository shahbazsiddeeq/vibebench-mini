def word_freq(text):
    """
    Returns a dict mapping each lowercase word to the number of times it occurs.
    A word is a maximal run of Unicode letters and digits.
    """
    if not text:
        return {}
    
    word_counts = {}
    current_word = []
    
    for char in text:
        if char.isalnum():  # Unicode letter or digit
            current_word.append(char)
        else:
            # We hit a separator
            if current_word:
                word = ''.join(current_word).lower()
                word_counts[word] = word_counts.get(word, 0) + 1
                current_word = []
    
    # Don't forget the last word if text doesn't end with a separator
    if current_word:
        word = ''.join(current_word).lower()
        word_counts[word] = word_counts.get(word, 0) + 1
    
    return word_counts
