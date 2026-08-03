def parse_duration(text: str) -> int:
    """
    Converts a compact duration string into a total number of seconds.

    The string consists of one or more consecutive segments, each a non-negative
    integer followed immediately by a single lowercase unit character:
    'w' (week), 'd' (day), 'h' (hour), 'm' (minute), 's' (second).
    Segments are summed. Units may appear in any order and may repeat.

    Args:
        text: The duration string to parse.

    Returns:
        The total duration in seconds as an integer.

    Raises:
        ValueError: If the input string does not fully match the specified grammar,
                    including empty string, bare numbers, units without numbers,
                    unknown units, or any stray/whitespace characters.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    if not text:
        raise ValueError("Input string cannot be empty.")

    unit_multipliers = {
        'w': 604800,  # 7 * 24 * 60 * 60
        'd': 86400,   # 24 * 60 * 60
        'h': 3600,    # 60 * 60
        'm': 60,
        's': 1,
    }

    total_seconds = 0
    current_pos = 0
    text_length = len(text)

    while current_pos < text_length:
        # Parse number part
        num_start = current_pos
        while current_pos < text_length and '0' <= text[current_pos] <= '9':
            current_pos += 1

        if current_pos == num_start:
            # No number found, or number is empty
            raise ValueError(f"Invalid duration format: expected a number at position {num_start}")

        try:
            # Using int() directly is safe here as we've already validated digits
            value = int(text[num_start:current_pos])
        except ValueError:
            # This should ideally not happen if the digit check is correct,
            # but as a safeguard.
            raise ValueError(f"Invalid number format at position {num_start}: '{text[num_start:current_pos]}'")

        # Parse unit part
        if current_pos >= text_length:
            raise ValueError(f"Invalid duration format: expected a unit after number '{value}' at position {current_pos}")

        unit_char = text[current_pos]
        current_pos += 1

        if unit_char not in unit_multipliers:
            raise ValueError(f"Invalid duration format: unknown unit '{unit_char}' at position {current_pos - 1}")

        total_seconds += value * unit_multipliers[unit_char]

    return total_seconds
