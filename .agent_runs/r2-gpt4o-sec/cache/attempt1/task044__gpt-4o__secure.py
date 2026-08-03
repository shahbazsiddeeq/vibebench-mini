# src/solution.py

import re

def to_snake(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Use regex to find patterns of uppercase letters followed by lowercase
    # or a single uppercase letter followed by lowercase letters
    pattern = re.compile(r'([A-Z]+)(?=[A-Z][a-z])|([A-Z][a-z]+)')
    
    def replace(match):
        # If the match is a full acronym, return it lowercased
        if match.group(1):
            return match.group(1).lower()
        # Otherwise, return the matched word lowercased
        return match.group(2).lower()
    
    # Replace matches with their snake_case equivalent
    snake = pattern.sub(replace, s)
    
    # Replace remaining uppercase letters with _lowercase
    snake = re.sub(r'([A-Z])', r'_\1', snake).lower()
    
    # Remove leading underscore if present
    return snake.lstrip('_')

def to_camel(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Split the string by underscores
    parts = s.split('_')
    
    # Capitalize the first letter of each part except the first one
    camel = parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])
    
    return camel
