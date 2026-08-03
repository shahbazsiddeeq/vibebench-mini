import re

def natural_sort(items):
    """
    Sorts a list of strings in natural order.

    Each embedded run of digits is compared by its numeric value, while runs
    of non-digit characters are compared character by character by Unicode
    code point. Letter comparison is case-sensitive. At the same position
    within a string, a numeric run sorts before a text run. The sort is stable.

    Args:
        items: A list of strings to be sorted.

    Returns:
        A new list containing the same strings sorted in natural order.
    """

    def get_key(text):
        # Split the string into parts: runs of digits and runs of non-digits.
        # The regex `(\d+)` captures one or more digits.
        # `re.split` will return a list where elements are either non-digit
        # parts or the captured digit parts.
        # Example: "file10.txt" -> ['', 'file', '10', '.', 'txt', '']
        # We need to filter out empty strings and convert digit parts to integers.
        parts = []
        for part in re.split(r'(\d+)', text):
            if part:  # Ignore empty strings that result from split
                if part.isdigit():
                    # Numeric runs sort before text runs.
                    # We use a tuple (0, int(part)) for numbers
                    # and (1, part) for text to ensure this order.
                    parts.append((0, int(part)))
                else:
                    parts.append((1, part))
        return parts

    # Use the custom key function for sorting.
    # The `sorted()` function is stable by default.
    return sorted(items, key=get_key)
