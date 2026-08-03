import re
from typing import List


def natural_sort(items: List[str]) -> List[str]:
    """
    Sort strings in natural order where numeric runs are compared by numeric value
    and text runs are compared lexicographically (case-sensitive).
    At the same position, numeric runs sort before text runs.
    The sort is stable.
    """
    
    def natural_key(s: str):
        """
        Convert a string into a tuple of comparable elements.
        Each element is either:
        - (0, int_value) for a numeric run (0 indicates numeric comes first)
        - (1, str_value) for a text run (1 indicates text comes second)
        """
        parts = []
        # Split the string into alternating text and digit runs
        for match in re.finditer(r'(\d+|[^\d]+)', s):
            token = match.group(0)
            if token.isdigit():
                # Numeric run: use (0, numeric_value) so numbers sort before text
                parts.append((0, int(token)))
            else:
                # Text run: use (1, text_value) so text sorts after numbers
                parts.append((1, token))
        return parts
    
    return sorted(items, key=natural_key)
