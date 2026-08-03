def caesar(text, shift):
    """
    Shifts letters in the given text by the specified shift amount (mod 26).
    Preserves case and leaves non-alphabetic characters unchanged.

    Args:
        text (str): The input string to be encrypted.
        shift (int): The number of positions to shift each letter.

    Returns:
        str: The encrypted string.
    """
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            shifted_char_code = ord('a') + (ord(char) - ord('a') + shift) % 26
            result.append(chr(shifted_char_code))
        elif 'A' <= char <= 'Z':
            shifted_char_code = ord('A') + (ord(char) - ord('A') + shift) % 26
            result.append(chr(shifted_char_code))
        else:
            result.append(char)
    return "".join(result)
