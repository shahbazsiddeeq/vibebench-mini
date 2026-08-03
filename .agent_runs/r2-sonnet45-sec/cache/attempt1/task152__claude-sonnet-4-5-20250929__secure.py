import re
from pathlib import Path


def parse_dotenv(path: str) -> dict[str, str]:
    """
    Parse a .env file (UTF-8) into a dict.
    
    Process the file line by line:
    - Strip each line; skip if empty or starts with '#'
    - Remove optional leading 'export ' prefix
    - Split on FIRST '=' into key and raw value
    - Validate key matches [A-Za-z_][A-Za-z0-9_]*
    - Process value based on quoting:
      - Double quotes: unescape \\n, \\t, \\r, \\\\, \\"
      - Single quotes: literal content
      - Unquoted: strip inline comments (# preceded by whitespace or at start), then strip whitespace
    - Later duplicate keys overwrite earlier ones
    
    Args:
        path: Path to .env file
        
    Returns:
        Dictionary of environment variables
        
    Raises:
        FileNotFoundError: If path does not exist
        ValueError: If line has no '=', empty key, or invalid key format
    """
    # Validate path exists
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    # Read file with UTF-8 encoding
    content = file_path.read_text(encoding='utf-8')
    
    result = {}
    key_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    
    for line in content.splitlines():
        # Strip whitespace
        stripped = line.strip()
        
        # Skip empty lines and full-line comments
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
        raw_value = stripped[eq_index + 1:]  # Everything after '='
        
        # Validate key
        if not key:
            raise ValueError(f"Empty key in line: {line}")
        if not key_pattern.match(key):
            raise ValueError(f"Invalid key format: {key}")
        
        # Process value based on quoting
        value = _process_value(raw_value)
        
        result[key] = value
    
    return result


def _process_value(raw_value: str) -> str:
    """
    Process the raw value based on quoting rules.
    
    Args:
        raw_value: The raw value string (everything after '=')
        
    Returns:
        Processed value string
    """
    # Check for double quotes
    if raw_value.startswith('"') and raw_value.endswith('"') and len(raw_value) >= 2:
        # Remove quotes and unescape
        quoted_content = raw_value[1:-1]
        return _unescape_double_quoted(quoted_content)
    
    # Check for single quotes
    if raw_value.startswith("'") and raw_value.endswith("'") and len(raw_value) >= 2:
        # Remove quotes and take literally
        return raw_value[1:-1]
    
    # Unquoted value
    # Strip inline comment: # at index 0 or preceded by whitespace
    value = _strip_inline_comment(raw_value)
    # Strip surrounding whitespace
    return value.strip()


def _unescape_double_quoted(s: str) -> str:
    """
    Unescape sequences in double-quoted strings.
    
    Handles: \\n, \\t, \\r, \\\\, \\"
    
    Args:
        s: String content (without surrounding quotes)
        
    Returns:
        Unescaped string
    """
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


def _strip_inline_comment(s: str) -> str:
    """
    Strip inline comment from unquoted value.
    
    The value ends just before the first '#' that is at index 0
    or immediately preceded by whitespace.
    
    Args:
        s: Unquoted value string
        
    Returns:
        String with inline comment removed
    """
    # Find first '#' at index 0 or preceded by whitespace
    for i, char in enumerate(s):
        if char == '#':
            if i == 0 or s[i - 1].isspace():
                return s[:i]
    
    return s
