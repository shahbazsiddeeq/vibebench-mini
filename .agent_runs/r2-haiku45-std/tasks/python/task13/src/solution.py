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
        s: Input string
        
    Returns:
        Slugified string, or empty string if no slug-able characters
    """
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
    
    # Keep only ASCII alphanumeric characters and spaces/hyphens
    # Replace any character that is not [a-z0-9] with a space
    ascii_only = ''.join(
        char if char in 'abcdefghijklmnopqrstuvwxyz0123456789' else ' '
        for char in lowercased
        if ord(char) < 128  # Keep only ASCII characters
    )
    
    # Replace runs of spaces/non-alphanumeric with single hyphen
    slugged = re.sub(r'\s+', '-', ascii_only)
    
    # Trim leading/trailing hyphens
    slugged = slugged.strip('-')
    
    return slugged
