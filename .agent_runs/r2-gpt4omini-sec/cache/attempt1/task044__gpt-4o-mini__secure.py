# src/solution.py

import re

def to_snake(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Match uppercase letters and handle acronyms
    s = re.sub(r'(?<!^)(?=[A-Z])', '_', s)  # Insert underscores before uppercase letters
    s = re.sub(r'([A-Z]+)(?=[A-Z][a-z])', r'\1_', s)  # Handle acronyms
    return s.lower()

def to_camel(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    parts = s.split('_')
    if not all(part.isidentifier() for part in parts):
        raise ValueError("Input must be a valid snake_case string.")
    
    return parts[0].lower() + ''.join(part.capitalize() for part in parts[1:])
