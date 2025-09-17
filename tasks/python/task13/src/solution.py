import re
import unicodedata


def slugify(s: str) -> str:
    # normalize + strip accents
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    # replace non-alnum with hyphen
    s = re.sub(r"[^a-z0-9]+", "-", s)
    # collapse hyphens and trim
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s
