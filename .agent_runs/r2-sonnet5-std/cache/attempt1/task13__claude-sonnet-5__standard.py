import re
import unicodedata


def slugify(s: str) -> str:
    if not s:
        return ""

    # Normalize to decomposed form and strip combining marks (accents)
    normalized = unicodedata.normalize("NFKD", s)
    stripped = "".join(c for c in normalized if not unicodedata.combining(c))

    # Encode to ASCII, dropping characters with no ASCII representation
    ascii_bytes = stripped.encode("ascii", "ignore")
    ascii_str = ascii_bytes.decode("ascii")

    # Lowercase
    lowered = ascii_str.lower()

    # Replace runs of non [a-z0-9] characters with a single hyphen
    slug = re.sub(r'[^a-z0-9]+', '-', lowered)

    # Trim leading/trailing hyphens
    slug = slug.strip('-')

    return slug
