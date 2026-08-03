def to_morse(text):
    """
    Encodes A-Z and 0-9 to Morse code.
    
    Args:
        text: String containing letters, digits, and whitespace
        
    Returns:
        Morse code string with letters separated by space and words by " / "
        
    Raises:
        ValueError: If text contains characters that are not letters, digits, or whitespace
    """
    MORSE_TABLE = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.",
    }
    
    # Split text into words by whitespace
    words = text.split()
    
    morse_words = []
    for word in words:
        morse_letters = []
        for char in word:
            # Convert to uppercase for lookup
            upper_char = char.upper()
            
            # Check if character is valid (letter or digit)
            if not (upper_char.isalpha() or upper_char.isdigit()):
                raise ValueError(f"Invalid character: {char}")
            
            # Check if character is in morse table
            if upper_char not in MORSE_TABLE:
                raise ValueError(f"Invalid character: {char}")
            
            morse_letters.append(MORSE_TABLE[upper_char])
        
        # Join letters within a word with single space
        morse_words.append(" ".join(morse_letters))
    
    # Join words with " / "
    return " / ".join(morse_words)
