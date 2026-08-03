# src/solution.py

def to_morse(text):
    import string

    FULL_TABLE = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.",
    }

    # Validate input
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Convert to uppercase to handle case insensitivity
    text = text.upper()

    # Check for invalid characters
    valid_chars = set(string.ascii_uppercase + string.digits + " ")
    if any(char not in valid_chars for char in text):
        raise ValueError("Input contains invalid characters.")

    # Encode to Morse code
    words = text.split()
    morse_words = []

    for word in words:
        morse_chars = [FULL_TABLE[char] for char in word]
        morse_words.append(" ".join(morse_chars))

    return " / ".join(morse_words)
