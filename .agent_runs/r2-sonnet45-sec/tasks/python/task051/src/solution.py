def normalize_case(text: str) -> str:
    """
    Normalize text case by lowercasing everything, then uppercasing the first
    alphabetic character of each sentence.
    
    A sentence starts at:
    - The beginning of the text
    - Immediately after any '.', '!', or '?'
    
    The first letter after such a boundary is capitalized, regardless of
    intervening spaces, quotes, or other non-letter characters.
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized text with proper sentence capitalization
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    if not text:
        return ""
    
    # First, lowercase the entire text
    result = list(text.lower())
    
    # Track whether we're at the start of a sentence
    at_sentence_start = True
    
    for i, char in enumerate(result):
        if at_sentence_start and char.isalpha():
            # Capitalize the first alphabetic character of the sentence
            result[i] = char.upper()
            at_sentence_start = False
        elif char in '.!?':
            # Mark that the next alphabetic character should be capitalized
            at_sentence_start = True
    
    return ''.join(result)
