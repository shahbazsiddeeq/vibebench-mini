"""Morse code encoder for ASCII letters and digits."""

_MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....",
    "7": "--...", "8": "---..", "9": "----.",
}


def to_morse(text: str) -> str:
    """Encode ASCII letters and digits as Morse code.

    Letters within words are separated by spaces, and whitespace-separated
    words are separated by ``" / "``.

    Raises:
        ValueError: If *text* contains anything other than ASCII letters,
            digits, or whitespace.
    """
    words = []
    current_word = []

    for character in text:
        if character.isspace():
            if current_word:
                words.append(" ".join(current_word))
                current_word = []
            continue

        code = _MORSE.get(character.upper())
        if code is None:
            raise ValueError(f"Unsupported character: {character!r}")
        current_word.append(code)

    if current_word:
        words.append(" ".join(current_word))

    return " / ".join(words)
