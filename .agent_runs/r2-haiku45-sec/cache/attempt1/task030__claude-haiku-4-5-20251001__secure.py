"""
Word Frequency Counter Module

This module provides a function to count word frequencies in text,
with Unicode-aware word boundary detection.
"""

import re
from typing import Dict


def word_freq(text: str) -> Dict[str, int]:
    """
    Count the frequency of words in the given text.
    
    A word is defined as a maximal run of Unicode letters and digits.
    All other characters (whitespace, punctuation, apostrophes, hyphens,
    underscores) act as separators and are not part of words.
    
    Words are converted to lowercase before counting.
    
    Args:
        text: The input text to analyze. Must be a string.
        
    Returns:
        A dictionary mapping lowercase words to their occurrence counts.
        Returns an empty dict if the input is empty or contains no words.
        
    Raises:
        TypeError: If text is not a string.
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    
    # Handle empty string
    if not text:
        return {}
    
    # Find all words: maximal runs of Unicode letters and digits
    # \w in Python regex with re.UNICODE matches Unicode letters, digits, and underscore
    # We need to match only letters and digits, so we use a more specific pattern
    # Using \p{L}\p{N} equivalent in Python: we match [^\W_] for letters/digits
    # Actually, simpler: match sequences of word characters that are not underscores
    # Or use: find all sequences of letters and digits
    
    # Pattern explanation:
    # [\w] matches word characters (letters, digits, underscore) in Unicode mode
    # We need to exclude underscores, so we use a negative approach
    # Better: use findall with pattern that matches letters and digits
    
    # Using re.findall with Unicode letter and digit pattern
    words = re.findall(r'[\p{L}\p{N}]+', text, flags=re.UNICODE) if hasattr(re, 'UNICODE') else None
    
    # Fallback for systems where \p{} might not work
    # Use a simpler approach: split on non-alphanumeric characters
    if words is None:
        # Match sequences of characters that are letters or digits
        # In Python regex, we can use character classes
        words = re.findall(r'[a-zA-Z0-9\u0080-\uffff]+', text)
    
    # Actually, let's use a more robust approach with re.findall
    # that properly handles Unicode letters and digits
    words = re.findall(r'[^\W_]+', text, flags=re.UNICODE)
    
    # Convert to lowercase and count
    freq_dict: Dict[str, int] = {}
    for word in words:
        word_lower = word.lower()
        freq_dict[word_lower] = freq_dict.get(word_lower, 0) + 1
    
    return freq_dict
