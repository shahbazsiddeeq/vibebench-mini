FULL_TABLE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
}

def to_morse(text: str) -> str:
    """
    Encodes A-Z and 0-9 to Morse code.
    Input is case-insensitive (lowercase letters encode the same as uppercase).
    Letters within a word are separated by a single space and words by " / " (splitting on whitespace).
    Raises ValueError for any character that is not a letter, digit, or whitespace.

    Args:
        text: The input string to encode.

    Returns:
        The Morse code representation of the input string.

    Raises:
        ValueError: If the input contains characters that are not letters, digits, or whitespace.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    words = text.split()
    morse_words = []

    for word in words:
        morse_chars = []
        for char in word:
            upper_char = char.upper()
            if upper_char in FULL_TABLE:
                morse_chars.append(FULL_TABLE[upper_char])
            else:
                raise ValueError(f"Invalid character '{char}' found in input. Only A-Z, 0-9, and whitespace are allowed.")
        morse_words.append(" ".join(morse_chars))

    return " / ".join(morse_words)
