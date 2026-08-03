import collections

def rle_encode(s: str) -> str:
    """
    Encodes consecutive runs of characters as count+char.
    The input must not contain ASCII digits (0-9).

    Args:
        s: The input string to encode.

    Returns:
        The run-length encoded string.

    Raises:
        ValueError: If the input string contains any ASCII digit.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    for char_code in s.encode('ascii', errors='ignore'):
        if ord('0') <= char_code <= ord('9'):
            raise ValueError("Input string must not contain ASCII digits (0-9).")

    if not s:
        return ""

    encoded_parts = []
    count = 0
    prev_char = ''

    for char in s:
        if char == prev_char:
            count += 1
        else:
            if prev_char:
                encoded_parts.append(str(count) + prev_char)
            count = 1
            prev_char = char
    
    if prev_char: # Append the last sequence
        encoded_parts.append(str(count) + prev_char)

    return "".join(encoded_parts)


def rle_decode(s: str) -> str:
    """
    Decodes a run-length encoded string.

    Args:
        s: The run-length encoded string.

    Returns:
        The decoded string.

    Raises:
        ValueError: If the input string is malformed.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    if not s:
        return ""

    decoded_parts = []
    i = 0
    n = len(s)

    while i < n:
        # Read count
        count_str = []
        while i < n and '0' <= s[i] <= '9':
            count_str.append(s[i])
            i += 1

        if not count_str:
            raise ValueError("Malformed input: expected digit for count.")

        try:
            count = int("".join(count_str))
        except ValueError:
            # This should ideally not happen if '0' <= s[i] <= '9' check is robust,
            # but good for defensive programming.
            raise ValueError("Malformed input: invalid count format.")

        if count == 0:
            raise ValueError("Malformed input: count cannot be zero.")

        # Read character
        if i >= n:
            raise ValueError("Malformed input: expected character after count.")

        char = s[i]
        i += 1

        # Check if the character is a digit, which is not allowed after a count
        if '0' <= char <= '9':
            raise ValueError("Malformed input: character after count cannot be a digit.")

        decoded_parts.append(char * count)

    return "".join(decoded_parts)
