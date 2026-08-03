import re
import unicodedata


def slugify(s: str) -> str:
    """
    Convert an input string into a lowercased ASCII slug.

    - Normalizes and strips accents from Latin characters (e.g. Crème -> Creme)
    - Lowercases the result
    - Replaces every run of non [a-z0-9] characters with a single hyphen
    - Trims leading/trailing hyphens
    - Characters with no ASCII representation (non-Latin scripts, emoji) are dropped
    - Returns "" if there is nothing sluggable (including for empty input)
    """
    if not isinstance(s, str):
        raise TypeError("slugify: input must be a string")

    # Normalize to NFKD form so accented Latin characters decompose into
    # a base ASCII character plus combining marks.
    normalized = unicodedata.normalize("NFKD", s)

    # Encode to ASCII, dropping anything that can't be represented
    # (combining accents, non-Latin scripts, emoji, etc.)
    ascii_bytes = normalized.encode("ascii", "ignore")
    ascii_str = ascii_bytes.decode("ascii")

    # Lowercase
    lowered = ascii_str.lower()

    # Replace runs of non [a-z0-9] characters with a single hyphen
    slug = re.sub(r"[^a-z0-9]+", "-", lowered)

    # Trim leading/trailing hyphens
    slug = slug.strip("-")

    return slug
