# src/solution.py

import unicodedata
import re

def slugify(s: str) -> str:
    # Normalize the string to decompose characters and remove accents
    normalized = unicodedata.normalize('NFD', s)
    # Encode to ASCII and ignore errors to drop non-ASCII characters
    ascii_only = normalized.encode('ascii', 'ignore').decode('utf-8')
    # Lowercase the string
    lowercased = ascii_only.lower()
    # Replace non-alphanumeric characters with a single hyphen
    slug = re.sub(r'[^a-z0-9]+', '-', lowercased)
    # Trim leading and trailing hyphens
    slug = slug.strip('-')
    return slug
