"""Sentence case normalization utilities."""


def normalize_case(text: str) -> str:
    """Lowercase text and capitalize the first alphabetic character per sentence.

    Sentences begin at the start of the text and after each period, exclamation
    mark, or question mark. Non-alphabetic characters between a sentence
    boundary and its first letter are preserved.

    Args:
        text: The string to normalize.

    Returns:
        The normalized string.

    Raises:
        TypeError: If *text* is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    result: list[str] = []
    awaiting_first_letter = True

    for character in text.lower():
        if awaiting_first_letter and character.isalpha():
            result.append(character.upper())
            awaiting_first_letter = False
        else:
            result.append(character)

        if character in ".!?":
            awaiting_first_letter = True

    return "".join(result)
