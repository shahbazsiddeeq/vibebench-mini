def parse_accept_language(value: str) -> list[tuple[str, float]]:
    if not value.strip():
        return []

    entries = value.split(',')
    parsed_entries = []

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        if ';' in entry:
            lang_range, q_part = entry.split(';', 1)
            lang_range = lang_range.strip().lower()
            q_part = q_part.strip()
            if not lang_range:
                raise ValueError("Empty language tag")
            if not q_part.lower().startswith('q='):
                raise ValueError("Unknown parameter name")
            try:
                quality = float(q_part[2:])
                if quality < 0 or quality > 1 or len(q_part[2:]) > 4 or (len(q_part[2:]) == 4 and q_part[2] != '0'):
                    raise ValueError("Quality value out of range")
            except ValueError:
                raise ValueError("Invalid quality value")
        else:
            lang_range = entry.strip().lower()
            quality = 1.0

        if quality > 0:
            parsed_entries.append((lang_range, quality))

    # Sort by quality descending, stable sort
    parsed_entries.sort(key=lambda x: -x[1])

    return parsed_entries
