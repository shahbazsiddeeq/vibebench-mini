# src/solution.py

def parse_accept_language(value: str) -> list[tuple[str, float]]:
    if not value.strip():
        return []

    entries = value.split(',')
    result = []

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        parts = entry.split(';')
        if len(parts) > 2:
            raise ValueError("Malformed entry with more than one ';'")

        lang_range = parts[0].strip().lower()
        if not lang_range:
            raise ValueError("Empty language tag")

        quality = 1.0
        if len(parts) == 2:
            q_part = parts[1].strip()
            if not q_part.lower().startswith('q='):
                raise ValueError("Unknown parameter name")
            try:
                quality = float(q_part[2:].strip())
            except ValueError:
                raise ValueError("Malformed q-parameter")
            if not (0 <= quality <= 1):
                raise ValueError("q-parameter out of range")

        if quality > 0:
            result.append((lang_range, quality))

    result.sort(key=lambda x: x[1], reverse=True)
    return result
