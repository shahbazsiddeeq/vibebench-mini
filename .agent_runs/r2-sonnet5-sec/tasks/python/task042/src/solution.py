"""
Word wrap utility.

Provides word_wrap(text, width) which wraps text into lines no longer
than `width` characters, without breaking words. Raises ValueError if
any single word exceeds the given width.
"""

from typing import List


def word_wrap(text: str, width: int) -> List[str]:
    """
    Wrap `text` into a list of lines each at most `width` characters long,
    without splitting words. Whitespace runs are treated as single
    separators.

    Args:
        text: The input text to wrap.
        width: Maximum line length (must be a positive integer).

    Returns:
        A list of strings, each of length <= width.

    Raises:
        TypeError: If text is not a str or width is not an int.
        ValueError: If width is not positive, or if any single word's
            length exceeds width.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an integer")
    if width <= 0:
        raise ValueError("width must be a positive integer")

    words = text.split()

    if not words:
        return []

    for word in words:
        if len(word) > width:
            raise ValueError(
                f"word exceeds maximum width of {width} characters"
            )

    lines: List[str] = []
    current_line: List[str] = []
    current_len = 0

    for word in words:
        word_len = len(word)
        if not current_line:
            current_line = [word]
            current_len = word_len
        else:
            # +1 for the space separator
            if current_len + 1 + word_len <= width:
                current_line.append(word)
                current_len += 1 + word_len
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_len = word_len

    if current_line:
        lines.append(" ".join(current_line))

    return lines
