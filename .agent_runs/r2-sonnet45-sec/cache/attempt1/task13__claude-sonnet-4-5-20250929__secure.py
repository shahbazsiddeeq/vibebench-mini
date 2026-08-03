import unicodedata
import re


def slugify(s):
    """
    Convert a string to a URL-friendly slug.
    
    Args:
        s: Input string to slugify
        
    Returns:
        Lowercased ASCII slug with hyphens separating words
    """
    if not isinstance(s, str):
        return ""
    
    # Normalize Unicode characters to decomposed form (NFD)
    # This separates base characters from combining marks (accents)
    normalized = unicodedata.normalize('NFD', s)
    
    # Filter out combining marks (accents) and keep only ASCII characters
    # Category 'Mn' is "Mark, nonspacing" which includes accents
    ascii_chars = []
    for char in normalized:
        # Keep only ASCII characters (ord < 128)
        # Skip combining marks
        if ord(char) < 128 and unicodedata.category(char) != 'Mn':
            ascii_chars.append(char)
    
    ascii_string = ''.join(ascii_chars)
    
    # Lowercase the string
    lowercased = ascii_string.lower()
    
    # Replace runs of non-alphanumeric characters with a single hyphen
    # [^a-z0-9]+ matches one or more characters that are NOT a-z or 0-9
    slug = re.sub(r'[^a-z0-9]+', '-', lowercased)
    
    # Trim leading and trailing hyphens
    slug = slug.strip('-')
    
    return slug
