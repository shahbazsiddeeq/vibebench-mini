def rle_encode(s: str) -> str:
    """
    Encodes consecutive runs of characters as count+char.
    Raises ValueError if the input contains any ASCII digit (0-9).
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    for char in s:
        if '0' <= char <= '9':
            raise ValueError("Input string must not contain digits.")

    if not s:
        return ""

    encoded_parts = []
    i = 0
    while i < len(s):
        current_char = s[i]
        count = 0
        j = i
        while j < len(s) and s[j] == current_char:
            count += 1
            j += 1
        encoded_parts.append(str(count) + current_char)
        i = j
    return "".join(encoded_parts)


def rle_decode(s: str) -> str:
    """
    Decodes a run-length encoded string.
    Raises ValueError for malformed input.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    if not s:
        return ""

    decoded_parts = []
    i = 0
    while i < len(s):
        # Read count
        count_str = []
        if not ('0' <= s[i] <= '9'):
            raise ValueError("Malformed input: expected digit for count.")
        while i < len(s) and '0' <= s[i] <= '9':
            count_str.append(s[i])
            i += 1

        if not count_str:
            raise ValueError("Malformed input: missing count.")

        count = int("".join(count_str))
        if count == 0:
            raise ValueError("Malformed input: count cannot be zero.")

        # Read character
        if i >= len(s):
            raise ValueError("Malformed input: expected character after count.")
        char = s[i]
        if '0' <= char <= '9':
            raise ValueError("Malformed input: character cannot be a digit.")
        i += 1

        decoded_parts.append(char * count)

    return "".join(decoded_parts)
