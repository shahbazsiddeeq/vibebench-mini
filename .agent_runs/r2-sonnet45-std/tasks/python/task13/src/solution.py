import unicodedata
import re


def slugify(s):
    """
    Convert a string to a lowercased ASCII slug.
    
    - Normalize and strip accents from Latin characters
    - Lowercase
    - Replace runs of non-[a-z0-9] characters with a single hyphen
    - Trim leading/trailing hyphens
    - Drop characters with no ASCII representation
    - Return "" if no slug-able characters remain
    """
    # Normalize Unicode characters to decomposed form (NFD)
    # This separates base characters from combining marks (accents)
    normalized = unicodedata.normalize('NFD', s)
    
    # Filter out combining marks (accents) and keep only ASCII characters
    # Category 'Mn' is "Mark, Nonspacing" which includes accents
    ascii_chars = []
    for char in normalized:
        if unicodedata.category(char) != 'Mn':
            # Try to encode as ASCII; if it fails, skip the character
            try:
                char.encode('ascii')
                ascii_chars.append(char)
            except UnicodeEncodeError:
                pass
    
    # Join the ASCII characters
    ascii_string = ''.join(ascii_chars)
    
    # Lowercase
    ascii_string = ascii_string.lower()
    
    # Replace runs of non-alphanumeric characters with a single hyphen
    # [^a-z0-9]+ matches one or more characters that are not a-z or 0-9
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_string)
    
    # Trim leading and trailing hyphens
    slug = slug.strip('-')
    
    return slug
