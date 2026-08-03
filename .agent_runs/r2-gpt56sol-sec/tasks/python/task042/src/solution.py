"""Utilities for wrapping text without splitting words."""

__all__ = ["word_wrap"]


def word_wrap(text: str, width: int) -> list[str]:
    """Wrap text greedily into lines no longer than ``width``.

    Whitespace between words is normalized to a single space. Empty or
    whitespace-only text produces an empty list.

    Raises:
        TypeError: If ``text`` is not a string or ``width`` is not an integer.
        ValueError: If ``width`` is not positive or a word exceeds ``width``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an integer")
    if width <= 0:
        raise ValueError("width must be greater than zero")

    words = text.split()
    if not words:
        return []

    if any(len(word) > width for word in words):
        raise ValueError("a word exceeds the specified width")

    lines: list[str] = []
    current_words: list[str] = []
    current_length = 0

    for word in words:
        required_length = len(word) if not current_words else current_length + 1 + len(word)

        if required_length <= width:
            current_words.append(word)
            current_length = required_length
        else:
            lines.append(" ".join(current_words))
            current_words = [word]
            current_length = len(word)

    if current_words:
        lines.append(" ".join(current_words))

    return lines
