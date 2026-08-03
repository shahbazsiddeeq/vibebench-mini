def caesar(text, shift):
    """
    Shifts letters in text by shift positions (mod 26).
    Preserves case and leaves non-alphabetic characters unchanged.
    
    Args:
        text: String to encode
        shift: Number of positions to shift (int)
    
    Returns:
        Encoded string with shifted letters
    """
    # Input validation
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(shift, int):
        raise TypeError("shift must be an integer")
    
    # Normalize shift to 0-25 range
    shift = shift % 26
    
    result = []
    
    for char in text:
        if char.isupper():
            # Shift uppercase letters
            shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(shifted)
        elif char.islower():
            # Shift lowercase letters
            shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result.append(shifted)
        else:
            # Leave non-alphabetic characters unchanged
            result.append(char)
    
    return ''.join(result)
