import re
from collections import Counter


def word_freq(text: str) -> dict[str, int]:
    """
    Count the frequency of words in the given text.
    
    A word is defined as a maximal run of Unicode letters and digits.
    All other characters are treated as separators.
    Words are converted to lowercase before counting.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary mapping each lowercase word to its occurrence count
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Pattern matches sequences of Unicode letters (\p{L}) and digits (\p{N})
    # Using \w would include underscores, which we don't want
    # [\p{L}\p{N}]+ would be ideal but Python's re doesn't support \p{} syntax
    # Instead, we use \w and then filter out underscores, or use a character class
    
    # Extract all sequences of letters (Unicode-aware) and digits
    # \w matches [a-zA-Z0-9_] plus Unicode letters, but includes underscore
    # We need to exclude underscore, so we use a negative lookahead or custom pattern
    
    # Using regex with Unicode flag to match letters and digits only
    # Pattern: one or more Unicode letters or digits
    words = re.findall(r'[\w]+', text, re.UNICODE)
    
    # Filter out words that are only underscores or contain underscores
    # Actually, \w includes underscores, so we need a different approach
    
    # Better approach: match sequences that are letters or digits, not underscores
    # We can use [^\W_] which means "not (non-word or underscore)" = "word char but not underscore"
    words = re.findall(r'[^\W_]+', text, re.UNICODE)
    
    # Convert to lowercase and count
    lowercase_words = [word.lower() for word in words]
    
    # Use Counter for efficient counting, then convert to regular dict
    return dict(Counter(lowercase_words))
