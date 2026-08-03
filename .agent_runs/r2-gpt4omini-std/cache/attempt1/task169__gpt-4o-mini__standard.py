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
            lang_range, q_part = entry.split(';', 1)
            if not lang_range:
                raise ValueError("Empty language tag")
            lang_range = lang_range.strip().lower()
            if not lang_range:
                raise ValueError("Empty language tag")
            if not q_part.lower().startswith('q='):
                raise ValueError("Unknown parameter name")
            q_value = q_part[2:].strip()
        else:
            lang_range = entry.strip().lower()
            q_value = '1.0'  # Default quality

        try:
            q_value_float = float(q_value)
        except ValueError:
            raise ValueError("Quality value must be a number")

        if not (0 <= q_value_float <= 1) or len(q_value.split('.')[-1]) > 3:
            raise ValueError("Quality value out of range")

        if q_value_float == 0:
            continue

        parsed_entries.append((lang_range, q_value_float))

    # Sort by quality descending, stable sort
    parsed_entries.sort(key=lambda x: x[1], reverse=True)
    
    return parsed_entries
