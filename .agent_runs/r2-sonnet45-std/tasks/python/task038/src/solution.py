def caesar(text, shift):
    """
    Applies Caesar cipher to text with given shift.
    
    Args:
        text: String to encode
        shift: Number of positions to shift (mod 26)
    
    Returns:
        Encoded string with letters shifted, case preserved, non-alpha unchanged
    """
    result = []
    
    for char in text:
        if char.isalpha():
            # Determine if uppercase or lowercase
            if char.isupper():
                # Shift within uppercase letters (A=65 to Z=90)
                base = ord('A')
                shifted = (ord(char) - base + shift) % 26
                result.append(chr(base + shifted))
            else:
                # Shift within lowercase letters (a=97 to z=122)
                base = ord('a')
                shifted = (ord(char) - base + shift) % 26
                result.append(chr(base + shifted))
        else:
            # Non-alphabetic characters remain unchanged
            result.append(char)
    
    return ''.join(result)
