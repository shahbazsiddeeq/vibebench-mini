import unicodedata
import re


def slugify(s: str) -> str:
    """
    slugify(s) -> lowercased ASCII slug. Normalize and strip accents from Latin
    characters (Crème -> creme), lowercase, then replace every run of characters
    that are not [a-z0-9] (spaces, punctuation, underscores, etc.) with a single
    hyphen, and trim leading/trailing hyphens. Characters that have no ASCII
    representation (non-Latin scripts, emoji) are dropped; a string with no
    slug-able characters (including the empty string) returns "". Example:
    slugify("Crème Brûlée 2025!") -> "creme-brulee-2025"
    """
    # Normalize to NFD (Canonical Decomposition) and strip accents
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    # Lowercase the string
    s = s.lower()

    # Replace non-alphanumeric characters with hyphens
    # Keep only a-z and 0-9, replace everything else with a hyphen
    s = re.sub(r'[^a-z0-9]+', '-', s)

    # Trim leading/trailing hyphens
    s = s.strip('-')

    return s
