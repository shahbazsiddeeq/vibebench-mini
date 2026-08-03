import unicodedata
import re


def slugify(s: str) -> str:
    """
    Convert a string to a lowercased ASCII slug.
    
    - Normalize and strip accents from Latin characters
    - Lowercase the string
    - Replace runs of non-alphanumeric characters with single hyphens
    - Trim leading/trailing hyphens
    - Drop characters with no ASCII representation
    
    Args:
        s: Input string to slugify
        
    Returns:
        Slugified string, or empty string if no slug-able characters exist
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    
    # Normalize to NFD (decomposed form) to separate base characters from accents
    normalized = unicodedata.normalize('NFD', s)
    
    # Remove combining marks (accents, diacritics)
    # Category 'Mn' = Mark, Nonspacing (combining marks)
    without_accents = ''.join(
        char for char in normalized 
        if unicodedata.category(char) != 'Mn'
    )
    
    # Lowercase
    lowercased = without_accents.lower()
    
    # Keep only ASCII alphanumeric characters and hyphens
    # Replace any character that is not [a-z0-9] with a space temporarily
    ascii_only = ''.join(
        char if char in 'abcdefghijklmnopqrstuvwxyz0123456789' else ' '
        for char in lowercased
    )
    
    # Replace runs of spaces (and other non-alphanumeric) with single hyphen
    # This regex matches one or more spaces
    with_hyphens = re.sub(r' +', '-', ascii_only)
    
    # Strip leading and trailing hyphens
    result = with_hyphens.strip('-')
    
    return result
