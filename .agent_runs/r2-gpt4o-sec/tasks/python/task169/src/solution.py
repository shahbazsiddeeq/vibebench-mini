# src/solution.py

def parse_accept_language(value: str) -> list[tuple[str, float]]:
    import re

    if not value.strip():
        return []

    entries = value.split(',')
    result = []

    q_value_pattern = re.compile(r'^\s*([^;]+)\s*(?:;\s*[qQ]\s*=\s*(\d(?:\.\d{1,3})?)\s*)?$')

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue

        match = q_value_pattern.match(entry)
        if not match:
            raise ValueError("Malformed entry")

        lang_range = match.group(1).strip().lower()
        q_value_str = match.group(2)

        if not lang_range:
            raise ValueError("Empty language tag")

        if q_value_str is None:
            q_value = 1.0
        else:
            try:
                q_value = float(q_value_str)
            except ValueError:
                raise ValueError("Non-numeric q-value")

            if not (0 <= q_value <= 1):
                raise ValueError("q-value out of range")

        if q_value > 0:
            result.append((lang_range, q_value))

    result.sort(key=lambda x: x[1], reverse=True)
    return result
