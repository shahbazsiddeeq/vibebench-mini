def parse_fixed_width(path: str, fields: list[tuple[str, int, int]]) -> list[dict[str, str]]:
    if not fields:
        raise ValueError("fields must not be empty")
    for name, start, length in fields:
        if start < 0 or length < 1:
            raise ValueError(f"invalid field spec: {(name, start, length)}")

    results = []
    with open(path, "r", encoding="utf-8", newline=None) as f:
        for line in f:
            stripped_line = line.rstrip("\n")
            if stripped_line.strip() == "":
                continue
            record = {}
            for name, start, length in fields:
                value = stripped_line[start:start+length].strip()
                record[name] = value
            results.append(record)
    return results
