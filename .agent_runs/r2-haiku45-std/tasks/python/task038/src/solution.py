def caesar(text, shift):
    """
    Shifts letters by shift (mod 26), preserves case, leaves non-alpha unchanged.
    
    Args:
        text: The input string to shift
        shift: The number of positions to shift (mod 26)
    
    Returns:
        The shifted string
    """
    result = []
    shift = shift % 26  # Handle shifts >= 26
    
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
            # Leave non-alpha characters unchanged
            result.append(char)
    
    return ''.join(result)
