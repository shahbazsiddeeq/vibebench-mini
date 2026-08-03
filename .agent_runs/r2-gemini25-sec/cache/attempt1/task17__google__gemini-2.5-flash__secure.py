import collections

def natural_sort(items):
    """
    Sorts a list of strings in natural order.

    Each embedded run of digits is compared by its numeric value, while runs of
    non-digit characters are compared character by character by Unicode code point.
    Letter comparison is case-sensitive. At the same position within a string,
    a numeric run sorts before a text run. The sort is stable.

    Args:
        items: A list of strings to be sorted.

    Returns:
        A new list containing the same strings sorted in natural order.

    Raises:
        TypeError: If items is not a list or contains non-string elements.
    """
    if not isinstance(items, list):
        raise TypeError("Input 'items' must be a list.")

    for item in items:
        if not isinstance(item, str):
            raise TypeError("All elements in 'items' must be strings.")

    def get_key(text):
        # This helper function converts a string into a list of (type, value) tuples
        # where type is 0 for numbers and 1 for text, and value is the parsed number
        # or the text segment. This allows for natural sorting.
        result = []
        i = 0
        while i < len(text):
            if text[i].isdigit():
                j = i
                while j < len(text) and text[j].isdigit():
                    j += 1
                result.append((0, int(text[i:j])))  # Type 0 for numbers
                i = j
            else:
                j = i
                while j < len(text) and not text[j].isdigit():
                    j += 1
                result.append((1, text[i:j]))  # Type 1 for text
                i = j
        return result

    # Use the stable sort property of Python's sorted()
    return sorted(items, key=get_key)
