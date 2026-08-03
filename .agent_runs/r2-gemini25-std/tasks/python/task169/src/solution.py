def parse_accept_language(value: str) -> list[tuple[str, float]]:
    """
    Parses an HTTP Accept-Language header into a list of (language_tag, quality) pairs
    sorted by quality DESCENDING, with ties kept in their original left-to-right order.
    """
    if not value or not value.strip():
        return []

    entries = value.split(',')
    parsed_languages = []

    for i, entry in enumerate(entries):
        entry = entry.strip()
        if not entry:
            continue

        parts = entry.split(';')
        lang_tag_part = parts[0].strip()

        if not lang_tag_part:
            raise ValueError("Empty language tag found in Accept-Language header.")

        lang_tag = lang_tag_part.lower()
        quality = 1.0

        if len(parts) > 1:
            for param_part in parts[1:]:
                param_part = param_part.strip()
                if not param_part:
                    continue

                if '=' not in param_part:
                    raise ValueError(f"Malformed parameter '{param_part}' in Accept-Language header.")

                param_name, param_value = param_part.split('=', 1)
                param_name = param_name.strip()
                param_value = param_value.strip()

                if param_name.lower() == 'q':
                    try:
                        q_val = float(param_value)
                    except ValueError:
                        raise ValueError(f"Invalid quality value '{param_value}' in Accept-Language header.")

                    if not (0 <= q_val <= 1):
                        raise ValueError(f"Quality value '{param_value}' out of range (0-1) in Accept-Language header.")

                    # Check for more than three decimal places
                    if '.' in param_value:
                        decimal_part = param_value.split('.')[1]
                        if len(decimal_part) > 3:
                            raise ValueError(f"Quality value '{param_value}' has more than three decimal places in Accept-Language header.")
                    
                    quality = q_val
                else:
                    raise ValueError(f"Unknown parameter '{param_name}' in Accept-Language header.")
        
        if quality > 0:
            parsed_languages.append((lang_tag, quality, i)) # Store original index for stable sort

    # Sort by quality descending, then by original index ascending (stable sort)
    parsed_languages.sort(key=lambda x: (-x[1], x[2]))

    return [(lang, q) for lang, q, _ in parsed_languages]
