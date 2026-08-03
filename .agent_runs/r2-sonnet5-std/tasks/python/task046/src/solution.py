# src/solution.py

MORSE_CODE_TABLE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
}


def to_morse(text: str) -> str:
    words = text.split()
    encoded_words = []
    for word in words:
        letters = []
        for ch in word:
            upper_ch = ch.upper()
            if upper_ch not in MORSE_CODE_TABLE:
                raise ValueError(f"Invalid character: {ch!r}")
            letters.append(MORSE_CODE_TABLE[upper_ch])
        encoded_words.append(" ".join(letters))
    return " / ".join(encoded_words)
