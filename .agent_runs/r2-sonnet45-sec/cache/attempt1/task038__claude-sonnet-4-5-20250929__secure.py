def caesar(text: str, shift: int) -> str:
    """
    Apply Caesar cipher to text with given shift.
    
    Shifts letters by shift positions (mod 26), preserves case,
    leaves non-alphabetic characters unchanged.
    
    Args:
        text: Input string to encode
        shift: Number of positions to shift (can be negative)
    
    Returns:
        Encoded string
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(shift, int):
        raise TypeError("shift must be an integer")
    
    # Normalize shift to 0-25 range
    shift = shift % 26
    
    result = []
    for char in text:
        if char.isalpha():
            # Determine if uppercase or lowercase
            if char.isupper():
                # Shift within uppercase A-Z range
                base = ord('A')
                shifted = (ord(char) - base + shift) % 26
                result.append(chr(base + shifted))
            else:
                # Shift within lowercase a-z range
                base = ord('a')
                shifted = (ord(char) - base + shift) % 26
                result.append(chr(base + shifted))
        else:
            # Non-alphabetic characters remain unchanged
            result.append(char)
    
    return ''.join(result)
