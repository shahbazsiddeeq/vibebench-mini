"""Unicode-aware word frequency counter."""

from collections import defaultdict


def word_freq(text: str) -> dict[str, int]:
    """Count lowercase words consisting of Unicode letters and digits."""
    counts: defaultdict[str, int] = defaultdict(int)
    current: list[str] = []

    for character in text:
        if character.isalnum():
            current.append(character)
        elif current:
            counts["".join(current).lower()] += 1
            current.clear()

    if current:
        counts["".join(current).lower()] += 1

    return dict(counts)
