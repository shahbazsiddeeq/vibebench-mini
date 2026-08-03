"""Utilities for wrapping text."""

from typing import List


def word_wrap(text: str, width: int) -> List[str]:
    """Wrap *text* into lines no longer than *width*, without splitting words.

    Whitespace between words is normalized to a single space. A ``ValueError``
    is raised if the width is not positive or if a word exceeds the width.
    """
    if width <= 0:
        raise ValueError("width must be positive")

    words = text.split()
    if any(len(word) > width for word in words):
        raise ValueError("a word exceeds the specified width")

    lines: List[str] = []
    current_words: List[str] = []
    current_length = 0

    for word in words:
        proposed_length = current_length + (1 if current_words else 0) + len(word)

        if proposed_length <= width:
            current_words.append(word)
            current_length = proposed_length
        else:
            lines.append(" ".join(current_words))
            current_words = [word]
            current_length = len(word)

    if current_words:
        lines.append(" ".join(current_words))

    return lines
