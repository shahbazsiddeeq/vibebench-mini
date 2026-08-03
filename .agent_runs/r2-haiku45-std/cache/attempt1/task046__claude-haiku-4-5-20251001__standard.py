def to_morse(text):
    """
    Encodes A-Z and 0-9 to Morse code.
    
    Args:
        text: A string containing letters, digits, and whitespace
        
    Returns:
        A string with Morse code representation
        
    Raises:
        ValueError: If text contains characters other than letters, digits, or whitespace
    """
    
    MORSE_CODE_TABLE = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.",
    }
    
    # Validate input - check for invalid characters
    for char in text:
        if not (char.isalpha() or char.isdigit() or char.isspace()):
            raise ValueError(f"Invalid character: {char}")
    
    # Convert to uppercase for processing
    text = text.upper()
    
    # Split by whitespace to get words
    words = text.split()
    
    # Process each word
    morse_words = []
    for word in words:
        morse_letters = []
        for char in word:
            if char in MORSE_CODE_TABLE:
                morse_letters.append(MORSE_CODE_TABLE[char])
        morse_words.append(" ".join(morse_letters))
    
    # Join words with " / "
    return " / ".join(morse_words)
