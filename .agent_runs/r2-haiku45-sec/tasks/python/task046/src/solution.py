def to_morse(text):
    """
    Encodes text to Morse code.
    
    Args:
        text: A string containing letters (A-Z), digits (0-9), and whitespace.
        
    Returns:
        A string with Morse code where letters/digits are separated by spaces
        and words are separated by " / ".
        
    Raises:
        ValueError: If text contains characters other than letters, digits, or whitespace.
    """
    # Morse code table
    morse_table = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.",
    }
    
    # Validate input: check for invalid characters
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
        morse_chars = []
        for char in word:
            if char in morse_table:
                morse_chars.append(morse_table[char])
        if morse_chars:  # Only add non-empty words
            morse_words.append(" ".join(morse_chars))
    
    # Join words with " / "
    return " / ".join(morse_words)
