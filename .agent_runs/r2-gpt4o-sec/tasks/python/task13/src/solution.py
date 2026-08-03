import unicodedata
import re

def slugify(s: str) -> str:
    # Normalize the string to NFKD form and encode to ASCII bytes, ignoring errors
    normalized = unicodedata.normalize('NFKD', s)
    ascii_bytes = normalized.encode('ascii', 'ignore')
    ascii_str = ascii_bytes.decode('ascii')
    
    # Convert to lowercase
    ascii_str = ascii_str.lower()
    
    # Replace non-alphanumeric characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_str)
    
    # Trim leading and trailing hyphens
    slug = slug.strip('-')
    
    return slug
