import re

def to_snake(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Use regex to find patterns of uppercase letters followed by lowercase
    # or end of string, and insert underscores appropriately
    s = re.sub(r'([a-z])([A-Z])', r'\1_\2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    
    return s.lower()

def to_camel(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    parts = s.split('_')
    # Capitalize all parts except the first one
    camel_case = parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])
    
    return camel_case
