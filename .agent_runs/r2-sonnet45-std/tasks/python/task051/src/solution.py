def normalize_case(text):
    """
    Lowercases the whole text, then uppercases the first alphabetic character
    of each sentence. A sentence starts at the beginning of the text and 
    immediately after any ., !, or ?.
    """
    if not text:
        return text
    
    # First, lowercase everything
    text = text.lower()
    
    # Convert to list for easier manipulation
    chars = list(text)
    
    # Track whether we're at the start of a sentence
    at_sentence_start = True
    
    for i, char in enumerate(chars):
        if at_sentence_start and char.isalpha():
            # Capitalize this letter and mark that we're no longer at sentence start
            chars[i] = char.upper()
            at_sentence_start = False
        elif char in '.!?':
            # Mark that the next letter should be capitalized
            at_sentence_start = True
    
    return ''.join(chars)
