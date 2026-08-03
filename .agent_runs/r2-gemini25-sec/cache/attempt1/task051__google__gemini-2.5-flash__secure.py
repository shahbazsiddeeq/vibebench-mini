import re

def normalize_case(text: str) -> str:
    """
    Normalizes the case of the input text by lowercasing the whole text,
    then uppercasing the first alphabetic character of each sentence.
    A sentence starts at the beginning of the text and immediately after
    any '.', '!', or '?'.

    Args:
        text: The input string to normalize.

    Returns:
        The case-normalized string.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if not text:
        return ""

    # Convert the entire text to lowercase first
    lower_text = list(text.lower())
    capitalize_next = True

    for i, char in enumerate(lower_text):
        if capitalize_next and char.isalpha():
            lower_text[i] = char.upper()
            capitalize_next = False
        elif char in ('.', '!', '?'):
            capitalize_next = True
        # If it's not an alphabetic character and not a sentence-ending punctuation,
        # and we are still looking for the first letter, keep capitalize_next as is.
        # If capitalize_next is False, it means we are inside a sentence, so no change.

    return "".join(lower_text)
