import re
import os

def parse_dotenv(path: str) -> dict[str, str]:
    """
    Parses a .env file (UTF-8) into a dict.

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

    result = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            original_line = line.strip()

            if not original_line or original_line.startswith('#'):
                continue

            # Remove optional 'export ' prefix
            if original_line.startswith('export '):
                line_content = original_line[len('export '):]
            else:
                line_content = original_line

            # Split on the FIRST '='
            parts = line_content.split('=', 1)
            if len(parts) != 2:
                raise ValueError(f"Line {line_num}: Missing '=' in '{original_line}'")

            key_raw, raw_value_unstripped = parts
            key = key_raw.strip()

            if not key:
                raise ValueError(f"Line {line_num}: Empty key in '{original_line}'")

            if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
                raise ValueError(f"Line {line_num}: Invalid key format '{key}'")

            value = ""
            if raw_value_unstripped.startswith('"') and raw_value_unstripped.endswith('"'):
                # Double-quoted value
                quoted_content = raw_value_unstripped[1:-1]
                value = (
                    quoted_content.replace('\\n', '\n')
                    .replace('\\t', '\t')
                    .replace('\\r', '\r')
                    .replace('\\\\', '\\')
                    .replace('\\"', '"')
                )
            elif raw_value_unstripped.startswith("'") and raw_value_unstripped.endswith("'"):
                # Single-quoted value
                value = raw_value_unstripped[1:-1]
            else:
                # Unquoted value
                # Strip inline comment
                processed_value = raw_value_unstripped
                comment_start_index = -1
                for i in range(len(processed_value)):
                    if processed_value[i] == '#':
                        if i == 0 or processed_value[i-1].isspace():
                            comment_start_index = i
                            break
                
                if comment_start_index != -1:
                    processed_value = processed_value[:comment_start_index]
                
                value = processed_value.strip()

            result[key] = value
    return result
