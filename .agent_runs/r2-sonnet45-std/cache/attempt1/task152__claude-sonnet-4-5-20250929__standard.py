import re
from pathlib import Path


def parse_dotenv(path: str) -> dict[str, str]:
    """Parse a .env file into a dictionary."""
    file_path = Path(path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    result = {}
    key_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Strip the line
            stripped = line.strip()
            
            # Skip empty lines or full-line comments
            if not stripped or stripped.startswith('#'):
                continue
            
            # Remove optional 'export ' prefix
            if stripped.startswith('export '):
                stripped = stripped[7:]  # len('export ') == 7
            
            # Split on first '='
            if '=' not in stripped:
                raise ValueError(f"Line missing '=': {line}")
            
            eq_index = stripped.index('=')
            key = stripped[:eq_index].strip()
            raw_value = stripped[eq_index + 1:]  # Don't strip yet!
            
            # Validate key
            if not key or not key_pattern.match(key):
                raise ValueError(f"Invalid key: {key}")
            
            # Process value based on quoting
            value = process_value(raw_value)
            
            result[key] = value
    
    return result


def process_value(raw_value: str) -> str:
    """Process the raw value according to quoting rules."""
    # Check if double-quoted
    if len(raw_value) >= 2 and raw_value[0] == '"' and raw_value[-1] == '"':
        # Double-quoted: unescape sequences
        inner = raw_value[1:-1]
        return unescape_double_quoted(inner)
    
    # Check if single-quoted
    elif len(raw_value) >= 2 and raw_value[0] == "'" and raw_value[-1] == "'":
        # Single-quoted: literal
        return raw_value[1:-1]
    
    else:
        # Unquoted: strip inline comments, then strip whitespace
        value = strip_inline_comment(raw_value)
        return value.strip()


def unescape_double_quoted(s: str) -> str:
    """Unescape sequences in double-quoted strings."""
    result = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            next_char = s[i + 1]
            if next_char == 'n':
                result.append('\n')
                i += 2
            elif next_char == 't':
                result.append('\t')
                i += 2
            elif next_char == 'r':
                result.append('\r')
                i += 2
            elif next_char == '\\':
                result.append('\\')
                i += 2
            elif next_char == '"':
                result.append('"')
                i += 2
            else:
                # Not a recognized escape sequence, keep as-is
                result.append(s[i])
                i += 1
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)


def strip_inline_comment(s: str) -> str:
    """Strip inline comment from unquoted value.
    
    The value ends just before the first '#' that is at index 0
    or immediately preceded by whitespace.
    """
    for i, char in enumerate(s):
        if char == '#':
            # Check if it's at index 0 or preceded by whitespace
            if i == 0 or s[i - 1].isspace():
                return s[:i]
    return s
