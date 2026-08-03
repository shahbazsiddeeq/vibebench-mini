import collections

def find_replace(text, replacements):
    """
    Applies all replacements simultaneously to the given text.
    Longer keys take priority over shorter overlapping keys.

    Args:
        text (str): The input string to perform replacements on.
        replacements (dict): A dictionary where keys are strings to find
                             and values are their replacements.

    Returns:
        str: The text after all simultaneous replacements have been applied.

    Raises:
        TypeError: If text is not a string or replacements is not a dictionary.
        ValueError: If any key in replacements is an empty string.
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")
    if not isinstance(replacements, dict):
        raise TypeError("Input 'replacements' must be a dictionary.")

    # Validate replacement keys and sort them by length (descending) for priority
    # and then alphabetically for stable tie-breaking.
    # This ensures longer keys are checked first.
    sorted_keys = sorted(
        [key for key in replacements if isinstance(key, str) and key],
        key=lambda k: (-len(k), k)
    )

    for key in sorted_keys:
        if not isinstance(replacements[key], str):
            raise TypeError(f"Replacement value for key '{key}' must be a string.")

    if not text or not replacements:
        return text

    # Use a list of characters to build the new string efficiently
    result_chars = []
    i = 0
    n = len(text)

    while i < n:
        found_match = False
        # Iterate through sorted keys to find the longest matching key first
        for original_key in sorted_keys:
            key_len = len(original_key)
            if text.startswith(original_key, i):
                # A match is found. Append its replacement.
                result_chars.append(replacements[original_key])
                i += key_len  # Move index past the matched key
                found_match = True
                break  # Move to the next part of the text after this replacement

        if not found_match:
            # No replacement key matched at the current position,
            # so append the original character and move to the next.
            result_chars.append(text[i])
            i += 1

    return "".join(result_chars)
