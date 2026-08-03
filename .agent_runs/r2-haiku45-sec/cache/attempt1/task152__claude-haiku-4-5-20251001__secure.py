import re
from pathlib import Path


def parse_dotenv(path: str) -> dict[str, str]:
    """
    Parse a .env file (UTF-8) into a dictionary.
    
    Args:
        path: Path to the .env file
        
    Returns:
        Dictionary mapping environment variable names to their values
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If a line has invalid syntax or key format
    """
    file_path = Path(path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    result = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Strip the line
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Remove optional leading 'export ' prefix
            if line.startswith('export '):
                line = line[7:]
            
            # Split on the FIRST '='
            if '=' not in line:
                raise ValueError(f"No '=' found in line: {line}")
            
            key, raw_value = line.split('=', 1)
            
            # Validate and strip key
            key = key.strip()
            if not key:
                raise ValueError("Empty key")
            
            # Validate key format: [A-Za-z_][A-Za-z0-9_]*
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', key):
                raise ValueError(f"Invalid key format: {key}")
            
            # Process value based on quoting
            value = _parse_value(raw_value)
            
            result[key] = value
    
    return result


def _parse_value(raw_value: str) -> str:
    """
    Parse the value part of a key=value pair.
    
    Args:
        raw_value: The raw right-hand side of the '='
        
    Returns:
        The processed value string
    """
    # Check for double-quoted value
    if raw_value.startswith('"') and raw_value.endswith('"'):
        # Remove quotes and unescape
        content = raw_value[1:-1]
        return _unescape_double_quoted(content)
    
    # Check for single-quoted value
    if raw_value.startswith("'") and raw_value.endswith("'"):
        # Remove quotes and take literally
        return raw_value[1:-1]
    
    # Unquoted value: strip inline comments and whitespace
    value = _strip_inline_comment(raw_value)
    value = value.strip()
    return value


def _unescape_double_quoted(content: str) -> str:
    """
    Unescape sequences in double-quoted strings.
    
    Handles: \\n, \\t, \\r, \\\\, \\"
    
    Args:
        content: The content between the quotes
        
    Returns:
        The unescaped string
    """
    result = []
    i = 0
    while i < len(content):
        if content[i] == '\\' and i + 1 < len(content):
            next_char = content[i + 1]
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
                # Unknown escape sequence, keep as-is
                result.append(content[i])
                i += 1
        else:
            result.append(content[i])
            i += 1
    
    return ''.join(result)


def _strip_inline_comment(value: str) -> str:
    """
    Strip inline comments from an unquoted value.
    
    A comment starts at index 0 or immediately after whitespace.
    
    Args:
        value: The unquoted value
        
    Returns:
        The value with inline comment removed
    """
    # Find the first '#' that is at index 0 or preceded by whitespace
    for i, char in enumerate(value):
        if char == '#':
            if i == 0 or value[i - 1].isspace():
                return value[:i]
    
    return value
