import re
import os

def parse_dotenv(path: str) -> dict[str, str]:
    """
    Parses a .env file (UTF-8) into a dict.

    Processes the file line by line. Strips each line; skips it if it is empty
    or if it begins with '#' (a full-line comment). Removes an optional leading
    'export ' prefix. Splits the remaining text on the FIRST '=' into key and
    raw value; if there is no '=', raises ValueError. The key is the text left
    of '=' stripped; raises ValueError if it is empty or does not match the
    regex [A-Za-z_][A-Za-z0-9_]*. Determines the value from the raw right-hand
    side (before any whitespace stripping) as follows: if it starts and ends
    with a double quote (\"), drop the quotes and unescape the sequences \\n,
    \\t, \\r, \\\\ and \\\" (no inline-comment stripping); if it starts and
    ends with a single quote ('), drop the quotes and take the contents
    literally; otherwise it is unquoted, so first strip an inline comment (the
    value ends just before the first '#' that is at index 0 or immediately
    preceded by whitespace), then strip surrounding whitespace. Later duplicate
    keys overwrite earlier ones.

    Args:
        path: The path to the .env file.

    Returns:
        A dictionary containing the parsed key-value pairs.

    Raises:
        FileNotFoundError: If `path` does not exist.
        ValueError: If a line is malformed (e.g., missing '=', invalid key).
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    result: dict[str, str] = {}
    key_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            stripped_line = line.strip()

            if not stripped_line or stripped_line.startswith('#'):
                continue

            # Remove 'export ' prefix
            if stripped_line.startswith('export '):
                stripped_line = stripped_line[len('export '):]

            # Find the first '='
            try:
                key_raw, raw_value = stripped_line.split('=', 1)
            except ValueError:
                raise ValueError(
                    f"Line {line_num}: Missing '=' in line: '{stripped_line}'"
                )

            key = key_raw.strip()
            if not key:
                raise ValueError(f"Line {line_num}: Empty key found.")
            if not key_pattern.match(key):
                raise ValueError(
                    f"Line {line_num}: Invalid key format: '{key}'"
                )

            value: str
            if raw_value.startswith('"') and raw_value.endswith('"'):
                # Double-quoted value
                content = raw_value[1:-1]
                # Unescape sequences: \\n, \\t, \\r, \\\\, \\"
                value = content.replace('\\n', '\n')
                value = value.replace('\\t', '\t')
                value = value.replace('\\r', '\r')
                value = value.replace('\\\\', '\\')
                value = value.replace('\\"', '"')
            elif raw_value.startswith("'") and raw_value.endswith("'"):
                # Single-quoted value
                value = raw_value[1:-1]
            else:
                # Unquoted value
                # Find inline comment: '#' preceded by whitespace or at index 0
                comment_start_index = -1
                for i in range(len(raw_value)):
                    if raw_value[i] == '#':
                        if i == 0 or raw_value[i-1].isspace():
                            comment_start_index = i
                            break
                
                if comment_start_index != -1:
                    value = raw_value[:comment_start_index].strip()
                else:
                    value = raw_value.strip()
            
            result[key] = value

    return result
