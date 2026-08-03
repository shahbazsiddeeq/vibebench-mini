import re

_Q_VALUE = re.compile(r"(?:0(?:\.[0-9]{1,3})?|1(?:\.0{1,3})?)")


def _parse_quality(text: str) -> float:
    """Parse a q-value token (0..1, <=3 decimals) into a float."""
    if not _Q_VALUE.fullmatch(text):
        raise ValueError(f"invalid q-value: {text!r}")
    return float(text)


def parse_accept_language(value: str) -> list[tuple[str, float]]:
    """Parse an Accept-Language header into sorted (tag, quality) pairs.

    Sorted by quality descending with stable ordering for ties. Tags are
    lowercased; quality defaults to 1.0; entries with q=0 are dropped.
    Raises ValueError on malformed entries.
    """
    if not isinstance(value, str):
        raise ValueError("value must be a string")
    items: list[tuple[str, float]] = []
    for entry in value.split(","):
        entry = entry.strip()
        if entry == "":
            continue
        segments = entry.split(";")
        tag = segments[0].strip().lower()
        if tag == "":
            raise ValueError("empty language tag")
        quality = 1.0
        if len(segments) == 1:
            pass
        elif len(segments) == 2:
            key, sep, qtext = segments[1].partition("=")
            if sep != "" and key.strip().lower() == "q":
                quality = _parse_quality(qtext.strip())
            else:
                raise ValueError(f"invalid parameter: {segments[1]!r}")
        else:
            raise ValueError(f"too many ';' segments: {entry!r}")
        if quality == 0.0:
            continue
        items.append((tag, quality))
    return sorted(items, key=lambda pair: pair[1], reverse=True)
