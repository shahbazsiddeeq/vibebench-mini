import os

def parse_fixed_width(path: str, fields: list[tuple[str, int, int]]) -> list[dict[str, str]]:
    """
    Reads the text file at `path` as UTF-8 using universal-newline mode and parses it
    as fixed-width records.

    Each `fields` entry is (name, start, length): a 0-based character offset and a
    character count. For every line, skip it if it is empty or contains only whitespace;
    otherwise build a dict where each field's value is line[start:start+length] with
    leading and trailing whitespace stripped (str.strip). Slicing past the end of a
    short line simply yields fewer characters (no error). Field order in the output
    dict follows the order of `fields`.

    Returns a list of these dicts, one per non-blank line, in file order.

    Raises FileNotFoundError if `path` does not exist.
    Raises ValueError if `fields` is empty or if any field has start < 0 or length < 1.
    """
    if not fields:
        raise ValueError("The 'fields' list cannot be empty.")

    for name, start, length in fields:
        if not isinstance(name, str) or not isinstance(start, int) or not isinstance(length, int):
            raise ValueError("Each field entry must be a tuple of (str, int, int).")
        if start < 0:
            raise ValueError(f"Field '{name}' has a negative start index: {start}")
        if length < 1:
            raise ValueError(f"Field '{name}' has a length less than 1: {length}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at path '{path}' does not exist.")
    if not os.path.isfile(path):
        # This handles cases where path exists but is not a regular file (e.g., a directory)
        raise FileNotFoundError(f"The path '{path}' is not a file.")

    parsed_records = []
    try:
        with open(path, 'r', encoding='utf-8', newline='') as f:
            for line in f:
                stripped_line = line.strip()
                if not stripped_line:
                    continue

                record = {}
                for name, start, length in fields:
                    end = start + length
                    field_value = line[start:end].strip()
                    record[name] = field_value
                parsed_records.append(record)
    except UnicodeDecodeError as e:
        # Catch potential encoding issues, though utf-8 is standard
        raise ValueError(f"Error decoding file '{path}' with UTF-8: {e}")
    except IOError as e:
        # Catch other potential I/O errors like permission denied
        raise IOError(f"An I/O error occurred while reading file '{path}': {e}")

    return parsed_records
