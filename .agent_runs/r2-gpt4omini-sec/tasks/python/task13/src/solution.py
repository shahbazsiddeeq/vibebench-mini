# src/solution.py

import unicodedata
import re

def slugify(s: str) -> str:
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    
    # Normalize the string to decompose characters with accents
    normalized = unicodedata.normalize('NFKD', s)
    
    # Encode to ASCII and decode back to ignore non-ASCII characters
    ascii_only = normalized.encode('ascii', 'ignore').decode('ascii')
    
    # Lowercase the string
    lowercased = ascii_only.lower()
    
    # Replace non-alphanumeric characters with a single hyphen
    slug = re.sub(r'[^a-z0-9]+', '-', lowercased)
    
    # Trim leading and trailing hyphens
    slug = slug.strip('-')
    
    return slug
