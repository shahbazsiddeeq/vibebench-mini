from typing import Final

_SENTENCE_ENDERS: Final[frozenset] = frozenset({".", "!", "?"})


def normalize_case(text: str) -> str:
    """
    Lowercase the entire text, then uppercase the first alphabetic character
    of each sentence. A sentence begins at the start of the text and
    immediately after any of '.', '!', or '?'. Non-letter characters
    (spaces, quotes, punctuation, etc.) between a sentence boundary and the
    first letter are left unchanged in place.

    Args:
        text: The input string to normalize.

    Returns:
        The normalized string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if text == "":
        return ""

    lowered = text.lower()
    result_chars = list(lowered)

    start_of_sentence = True
    for i, ch in enumerate(result_chars):
        if start_of_sentence and ch.isalpha():
            result_chars[i] = ch.upper()
            start_of_sentence = False
        elif ch in _SENTENCE_ENDERS:
            start_of_sentence = True

    return "".join(result_chars)
