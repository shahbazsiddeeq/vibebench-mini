# src/solution.py

from typing import List, Tuple
import re

def parse_accept_language(value: str) -> List[Tuple[str, float]]:
    if not value.strip():
        return []

    entries = value.split(',')
    parsed_entries = []

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        # Match lang-range and optional q-value
        match = re.match(r'^(.*?)(;q=([0-1](?:\.[0-9]{1,3})?))?$', entry, re.IGNORECASE)
        if not match:
            raise ValueError("Malformed entry")

        lang_range = match.group(1).strip().lower()
        q_value = match.group(3)

        if not lang_range:
            raise ValueError("Empty language tag")

        if q_value is None:
            quality = 1.0
        else:
            try:
                quality = float(q_value)
                if quality < 0 or quality > 1:
                    raise ValueError("Quality out of range")
            except ValueError:
                raise ValueError("Invalid quality value")

        if quality == 0:
            continue

        parsed_entries.append((lang_range, quality))

    # Sort by quality descending, stable sort
    parsed_entries.sort(key=lambda x: x[1], reverse=True)

    return parsed_entries
