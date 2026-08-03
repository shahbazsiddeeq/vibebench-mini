def caesar(text: str, shift: int) -> str:
    """
    Encrypts or decrypts a string using the Caesar cipher.

    Args:
        text: The input string to be processed.
        shift: The integer shift value.

    Returns:
        The processed string.
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")
    if not isinstance(shift, int):
        raise TypeError("Input 'shift' must be an integer.")

    result = []
    # Ensure shift is within a reasonable range for modulo operation
    # and handle negative shifts correctly.
    shift = shift % 26

    for char in text:
        if 'a' <= char <= 'z':
            shifted_char_code = ord(char) + shift
            if shifted_char_code > ord('z'):
                shifted_char_code -= 26
            elif shifted_char_code < ord('a'): # Handle negative shifts that wrap below 'a'
                shifted_char_code += 26
            result.append(chr(shifted_char_code))
        elif 'A' <= char <= 'Z':
            shifted_char_code = ord(char) + shift
            if shifted_char_code > ord('Z'):
                shifted_char_code -= 26
            elif shifted_char_code < ord('A'): # Handle negative shifts that wrap below 'A'
                shifted_char_code += 26
            result.append(chr(shifted_char_code))
        else:
            result.append(char)
    return "".join(result)
