# src/solution.py

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
            parts = entry.split(';', 1)
            if len(parts) != 2:
                raise ValueError("Malformed entry: more than one ';' segment")
            lang_range, q_part = parts
        else:
            lang_range, q_part = entry, None

        lang_range = lang_range.strip().lower()
        if not lang_range:
            raise ValueError("Empty language tag")

        if q_part is not None:
            q_part = q_part.strip().lower()
            if not q_part.startswith('q='):
                raise ValueError("Unknown parameter name")
            q_value = q_part[2:]

            try:
                quality = float(q_value)
            except ValueError:
                raise ValueError("Non-numeric q value")
            
            if quality < 0 or quality > 1 or len(q_value.split('.')[1]) > 3:
                raise ValueError("q value out of range")
        else:
            quality = 1.0

        if quality > 0:
            parsed_entries.append((lang_range, quality))

    # Sort by quality descending, stable sort
    parsed_entries.sort(key=lambda x: -x[1])
    return parsed_entries
