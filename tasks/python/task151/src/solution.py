def parse_fixed_width(
    path: str, fields: list[tuple[str, int, int]]
) -> list[dict[str, str]]:
    """Parse a fixed-width text file into a list of field dicts."""
    if not fields:
        raise ValueError("fields must not be empty")
    for name, start, length in fields:
        if start < 0:
            raise ValueError(f"field {name!r} has negative start {start}")
        if length < 1:
            raise ValueError(f"field {name!r} has length {length} < 1")

    records: list[dict[str, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n").rstrip("\r")
            if not line.strip():
                continue
            record: dict[str, str] = {}
            for name, start, length in fields:
                record[name] = line[start:start + length].strip()
            records.append(record)
    return records
