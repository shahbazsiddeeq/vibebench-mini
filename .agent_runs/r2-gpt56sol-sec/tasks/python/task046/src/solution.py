"""Morse code encoder for ASCII letters and digits."""

_MORSE_TABLE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
}


def to_morse(text: str) -> str:
    """Encode ASCII letters and digits as Morse code.

    Letters within words are separated by spaces, while words are separated
    by ``" / "``. Any Unicode whitespace is accepted as a word separator.

    Args:
        text: Text containing only ASCII letters, digits, and whitespace.

    Returns:
        The Morse code representation of ``text``.

    Raises:
        TypeError: If ``text`` is not a string.
        ValueError: If ``text`` contains an unsupported character.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    for character in text:
        if not character.isspace() and character.upper() not in _MORSE_TABLE:
            raise ValueError("text contains an unsupported character")

    return " / ".join(
        " ".join(_MORSE_TABLE[character.upper()] for character in word)
        for word in text.split()
    )
