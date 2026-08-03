def parse_duration(text: str) -> int:
    """
    Converts a compact duration string into a total number of seconds.

    The string is one or more consecutive segments, each a non-negative integer
    followed immediately by a single lowercase unit character:
    'w'=604800s (week), 'd'=86400s (day), 'h'=3600s (hour), 'm'=60s (minute), 's'=1s (second).
    Segments are simply summed.

    Args:
        text: The duration string to parse.

    Returns:
        The total duration in seconds.

    Raises:
        ValueError: If the input string does not fully match the grammar,
                    including empty string, bare number, unit with no number,
                    unknown unit, or any stray/whitespace character.
    """
    if not text:
        raise ValueError("Input string cannot be empty.")

    unit_multipliers = {
        'w': 604800,  # week
        'd': 86400,   # day
        'h': 3600,    # hour
        'm': 60,      # minute
        's': 1        # second
    }

    total_seconds = 0
    i = 0
    n = len(text)

    while i < n:
        # Parse number part
        start_num = i
        while i < n and text[i].isdigit():
            i += 1
        
        if i == start_num:  # No digits found
            raise ValueError(f"Expected a number at position {start_num}, but found '{text[start_num:]}'")

        num_str = text[start_num:i]
        try:
            value = int(num_str)
        except ValueError: # Should not happen if text[i].isdigit() check is correct, but good for robustness
            raise ValueError(f"Invalid number format: '{num_str}'")

        # Parse unit part
        if i >= n:  # Number without a unit
            raise ValueError(f"Expected a unit after number '{num_str}' at position {i}, but found end of string.")
        
        unit_char = text[i]
        i += 1

        if unit_char not in unit_multipliers:
            raise ValueError(f"Unknown or invalid unit '{unit_char}' at position {i-1}. Expected one of {list(unit_multipliers.keys())}.")
        
        if not unit_char.islower():
             raise ValueError(f"Invalid unit case '{unit_char}' at position {i-1}. Units must be lowercase.")

        total_seconds += value * unit_multipliers[unit_char]

    return total_seconds
