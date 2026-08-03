"""
Find and Replace (Simultaneous) module.

Applies all replacements simultaneously to text, with longer keys taking
priority over shorter overlapping keys.
"""

from typing import Dict


def find_replace(text: str, replacements: Dict[str, str]) -> str:
    """
    Apply all replacements simultaneously to text.
    
    Longer keys take priority over shorter overlapping keys.
    Replacements are applied simultaneously, not sequentially (no chaining).
    
    Args:
        text: The input text to perform replacements on.
        replacements: A dictionary mapping search strings to replacement strings.
    
    Returns:
        The text with all replacements applied simultaneously.
    
    Raises:
        TypeError: If text is not a string or replacements is not a dict.
        ValueError: If any key or value in replacements is not a string.
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(replacements, dict):
        raise TypeError("replacements must be a dictionary")
    
    for key, value in replacements.items():
        if not isinstance(key, str):
            raise ValueError("all keys in replacements must be strings")
        if not isinstance(value, str):
            raise ValueError("all values in replacements must be strings")
    
    # Handle empty cases
    if not text or not replacements:
        return text
    
    # Sort keys by length (descending) to prioritize longer matches
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
    
    result = []
    i = 0
    
    while i < len(text):
        matched = False
        
        # Try to match the longest keys first
        for key in sorted_keys:
            if text[i:i + len(key)] == key:
                result.append(replacements[key])
                i += len(key)
                matched = True
                break
        
        # If no key matched, keep the original character
        if not matched:
            result.append(text[i])
            i += 1
    
    return "".join(result)
