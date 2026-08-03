import re
import unicodedata


def slugify(s: str) -> str:
    normalized = unicodedata.normalize("NFKD", s)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
