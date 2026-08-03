def normalize_case(text: str) -> str:
    """
    Normalize text to sentence case.
    
    Lowercases the whole text, then uppercases the first alphabetic character
    of each sentence. A sentence starts at the beginning of the text and 
    immediately after any ., !, or ?. The first letter to appear after such 
    a boundary is capitalized regardless of any intervening spaces, quotes, 
    or other non-letter characters.
    
    Args:
        text: The input text to normalize
        
    Returns:
        The normalized text in sentence case
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    if not text:
        return text
    
    # Convert entire text to lowercase
    text = text.lower()
    
    # Convert to list for easier manipulation
    chars = list(text)
    
    # Track if we're at the start of a sentence
    at_sentence_start = True
    
    for i, char in enumerate(chars):
        if at_sentence_start and char.isalpha():
            # Capitalize the first alphabetic character of the sentence
            chars[i] = char.upper()
            at_sentence_start = False
        elif char in '.!?':
            # Mark that the next alphabetic character starts a new sentence
            at_sentence_start = True
    
    return ''.join(chars)
