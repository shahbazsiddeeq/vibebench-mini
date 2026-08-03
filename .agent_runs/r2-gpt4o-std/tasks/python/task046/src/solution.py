# src/solution.py

FULL_TABLE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
}

def to_morse(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    text = text.upper()
    words = text.split()
    
    morse_words = []
    for word in words:
        morse_chars = []
        for char in word:
            if char in FULL_TABLE:
                morse_chars.append(FULL_TABLE[char])
            else:
                raise ValueError(f"Invalid character: {char}")
        morse_words.append(" ".join(morse_chars))
    
    return " / ".join(morse_words)
