def to_morse(text):
    """
    Encodes text to Morse code.
    
    Args:
        text: String containing only letters (A-Z, case-insensitive), digits (0-9), 
              and whitespace
    
    Returns:
        String with Morse code representation
        
    Raises:
        ValueError: If text contains invalid characters
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
    
    # Validate input - only allow letters, digits, and whitespace
    for char in text:
        if not (char.isalpha() or char.isdigit() or char.isspace()):
            raise ValueError(f"Invalid character: {char}")
    
    # Convert to uppercase for processing
    text = text.upper()
    
    # Split into words by whitespace
    words = text.split()
    
    # Process each word
    morse_words = []
    for word in words:
        morse_chars = []
        for char in word:
            if char in MORSE_TABLE:
                morse_chars.append(MORSE_TABLE[char])
            else:
                # This shouldn't happen if validation is correct, but be safe
                raise ValueError(f"Character not in Morse table: {char}")
        
        # Join characters in a word with single space
        morse_words.append(" ".join(morse_chars))
    
    # Join words with " / "
    return " / ".join(morse_words)
