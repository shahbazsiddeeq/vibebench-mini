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

def to_morse(text: str) -> str:
    morse_code = []
    words = text.split(' ')
    
    for word in words:
        encoded_word = []
        for char in word:
            upper_char = char.upper()
            if upper_char in FULL_TABLE:
                encoded_word.append(FULL_TABLE[upper_char])
            else:
                raise ValueError(f"Invalid character: {char}")
        morse_code.append(" ".join(encoded_word))
    
    return " / ".join(morse_code)
