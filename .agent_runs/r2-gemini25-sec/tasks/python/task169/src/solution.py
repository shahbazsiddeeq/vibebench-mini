import collections

def parse_accept_language(value: str) -> list[tuple[str, float]]:
    """
    Parses an HTTP Accept-Language header into a list of (language_tag, quality) pairs.

    Args:
        value: The Accept-Language header string.

    Returns:
        A list of (language_tag, quality) pairs, sorted by quality descending,
        with ties kept in their original left-to-right order.

    Raises:
        ValueError: If the header is malformed (e.g., invalid q-value,
                    empty language tag, unknown parameter, multiple semicolons).
    """
    if not isinstance(value, str):
        raise TypeError("Input 'value' must be a string.")

    value = value.strip()
    if not value:
        return []

    entries = value.split(',')
    parsed_languages = []

    for original_index, entry_str in enumerate(entries):
        entry_str = entry_str.strip()
        if not entry_str:
            continue

        parts = entry_str.split(';')
        if len(parts) > 2:
            raise ValueError(f"Malformed Accept-Language entry: too many semicolons in '{entry_str}'")

        lang_tag_raw = parts[0].strip()
        if not lang_tag_raw:
            raise ValueError(f"Malformed Accept-Language entry: empty language tag in '{entry_str}'")

        lang_tag = lang_tag_raw.lower() if lang_tag_raw != '*' else '*'
        quality = 1.0

        if len(parts) == 2:
            param_str = parts[1].strip()
            if not param_str:
                raise ValueError(f"Malformed Accept-Language entry: empty parameter after semicolon in '{entry_str}'")

            if not param_str.lower().startswith('q='):
                raise ValueError(f"Malformed Accept-Language entry: unknown parameter '{param_str}' in '{entry_str}'")

            q_value_str = param_str[2:].strip()
            if not q_value_str:
                raise ValueError(f"Malformed Accept-Language entry: empty q-value in '{entry_str}'")

            try:
                q_value = float(q_value_str)
            except ValueError:
                raise ValueError(f"Malformed Accept-Language entry: non-numeric q-value '{q_value_str}' in '{entry_str}'")

            # Validate q-value range and precision
            if not (0.0 <= q_value <= 1.0):
                raise ValueError(f"Malformed Accept-Language entry: q-value '{q_value_str}' out of range [0, 1] in '{entry_str}'")

            # Check for more than 3 decimal places
            if '.' in q_value_str:
                decimal_part = q_value_str.split('.')[1]
                if len(decimal_part) > 3:
                    raise ValueError(f"Malformed Accept-Language entry: q-value '{q_value_str}' has more than 3 decimal places in '{entry_str}'")
            
            quality = q_value
        
        if quality > 0:
            parsed_languages.append((lang_tag, quality, original_index))

    # Sort by quality (descending), then by original_index (ascending for stable sort)
    parsed_languages.sort(key=lambda x: (-x[1], x[2]))

    return [(lang, q) for lang, q, _ in parsed_languages]
