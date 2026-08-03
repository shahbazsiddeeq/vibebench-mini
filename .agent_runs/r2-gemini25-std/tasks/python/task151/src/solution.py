def parse_fixed_width(path: str, fields: list[tuple[str, int, int]]) -> list[dict[str, str]]:
    """
    Reads the text file at `path` as UTF-8 using universal-newline mode and
    parses it as fixed-width records.

    Each `fields` entry is (name, start, length): a 0-based character offset
    and a character count. For every line, skip it if it is empty or contains
    only whitespace; otherwise build a dict where each field's value is
    line[start:start+length] with leading and trailing whitespace stripped
    (str.strip). Slicing past the end of a short line simply yields fewer
    characters (no error). Field order in the output dict follows the order
    of `fields`.

    Returns a list of these dicts, one per non-blank line, in file order.

    Raises FileNotFoundError if `path` does not exist.
    Raises ValueError if `fields` is empty or if any field has start < 0 or length < 1.
    """
    if not fields:
        raise ValueError("`fields` cannot be empty.")

    for name, start, length in fields:
        if start < 0:
            raise ValueError(f"Field '{name}' has a negative start offset: {start}")
        if length < 1:
            raise ValueError(f"Field '{name}' has a length less than 1: {length}")

    records = []
    with open(path, 'r', encoding='utf-8', newline=None) as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line:
                continue

            record = {}
            for name, start, length in fields:
                end = start + length
                field_value = line[start:end].strip()
                record[name] = field_value
            records.append(record)

    return records
