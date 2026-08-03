# src/solution.py

import re

def normalize_case(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    # Lowercase the entire text
    text = text.lower()
    
    # Function to capitalize the first letter after a sentence-ending punctuation
    def capitalize_first_letter(match):
        return match.group(0) + match.group(1).capitalize() if match.group(1) else match.group(0)

    # Regular expression to find sentence boundaries and the first letter after them
    pattern = r'([.!?]\s*|^)([\'"’]*)([a-z])'
    
    # Use re.sub to apply the capitalization function
    normalized_text = re.sub(pattern, lambda m: capitalize_first_letter(m), text)
    
    return normalized_text
